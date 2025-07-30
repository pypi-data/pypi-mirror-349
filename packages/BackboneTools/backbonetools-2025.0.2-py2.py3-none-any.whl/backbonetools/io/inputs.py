"""Functions for processing backbone input data"""
# backbonetools - create, modify and visualise input and output data for the esm backbone and run backbone
# Copyright (C) 2020-2025 Leonie Plaga, David Huckebrink, Christine Nowak, Jan Mutke, Jonas Finke, Silke Johanndeiter, Sophie Pathe

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess as sp
import warnings
from functools import partial, reduce
from io import StringIO
from itertools import groupby
from pathlib import Path
import os

import pandas as pd
import tsam.timeseriesaggregation as tsam
from gams import GamsDatabase, GamsException, GamsSetRecord, GamsWorkspace


class BackboneInput:
    """A class to convert an input file to pandas dataframes and work with it (e.g. time series aggregation via tsam)
    """   
    
    def __init__(self, path):
        """initializes class by converting gdx file to dictionary of pandas dataframes

        Args:
            path (str): path to input file

        Raises:
            FileNotFoundError: If path to input file was not found
        """        
        # this section is redundant with results.BackboneResult
        ws = GamsWorkspace(".")

        self._path = Path(path).absolute()

        if not self._path.exists():
            raise FileNotFoundError(self._path)

        self.gams_db = ws.add_database_from_gdx(self._path.as_posix())

        self.set_symbols_as_attribs()

    @property
    def input_symbols(self):
        """gets all symbols from the input file

        Raises:
            ge: if something is wrong with the length of the file

        Returns:
            list: list of all symbols in input file
        """        
        if hasattr(self, "_symbols"):
            return self._symbols
        # list comprehension of gams_db raises an exception at the last index
        symbols = []
        try:
            for p in self.gams_db:
                symbols.append(p.name)
        except GamsException as ge:
            if "out of range" in str(ge) and str(self.gams_db.number_symbols) in str(
                ge
            ):
                pass
            else:
                raise ge
        self._symbols = symbols
        return symbols

    def set_symbols_as_attribs(self):      
        """
        Sets all input symbols as methods. Allows for easy access like
        `bb_input.p_gnu_io()` or `bb_input.ts_influx()`"""
        for symbol in self.input_symbols:
            setattr(self, symbol, partial(self.param_as_df_gdxdump, symbol))

    def param_as_df_gdxdump(
        self, symbol, encoding="1252", convert_time=True
    ) -> pd.DataFrame:
        """Use the 'gdxdump' GAMS utility via subprocess to convert a parameter into a pd.DataFrame.
        This is sometimes beneficial, to circumvent decoding errors

        Returns:
            pandas.dataframe: parameter converted to a pandas dataframe
        """        
        gdxdump = sp.run(
            ["gdxdump", self._path, "format", "csv", "symb", symbol], stdout=sp.PIPE
        )
        csv_data = gdxdump.stdout.decode(encoding=encoding)
        header = csv_data.partition("\n")[0]

        header = [x.strip('"') for x in header.split(",")]
        dtypes = [str if x != "Val" else float for x in header]
        dtypes = dict(zip(header, dtypes))
        df = pd.read_csv(StringIO(csv_data), dtype=dtypes, na_values="Eps")

        if df.empty:
            return df

        # converts the time column to int by omitting the first character
        try:
            if convert_time:
                if "t" in df.columns:
                    df["t"] = df["t"].apply(lambda t: int(t[1:]))
                else:
                    # for backbone inputs, the index is ["Dim1", "Dim2", ... , "Val"], but there might be a time column
                    first_row = df.loc[0]
                    is_time = first_row.apply(lambda x: str(x).startswith("t000"))

                    if any(is_time):
                        # any is necessary, otherwise *.idxmax()  simply returns first element
                        time_col = is_time.idxmax()  # should be something like "Dim4"
                        df[time_col] = df[time_col].apply(lambda t: int(t[1:]))
                        df.rename({time_col: "t"}, axis=1, inplace=True)
        except Exception as e:
            print(f"Error during time conversion for {symbol=}, {df=}")

        return df

    def update_gams_parameter_in_db(
        self,
        param_name: str,
        indices: list,
        value: float = None,
        apply_percentage: float = None,
    ) -> GamsDatabase:
        """change gams parameter in a database

        Args:
            param_name (str): name of parameter to change
            indices (list): index of value to be changed
            value (float, optional): new value. Defaults to None.
            apply_percentage (float, optional): give new value as percentage of old value. Defaults to None.

        Raises:
            ge: if record cannot be found
            ValueError: if neither value nor percentage are passed

        Returns:
            GamsDatabase: gams databased with changed value
        """        
        # note that you are always only working on the same instance of the database.
        # retrieve the parameter i.e. "p_groupPolicyEmission"
        parameter = self.gams_db.get_symbol(param_name)

        # retrieve the record from that parameter i.e. ["emission group", "emissionCap", "CO2"]
        try:
            record = parameter.find_record(indices)
        except GamsException as ge:
            if "Cannot find" in ge.value:
                # This is potentially dangerous since any index value can be added.
                # However, in the case of a bad index, GAMS should throw a DomainViolationError
                warnings.warn(
                    f"Warning: Caught 'GamsException: {ge.value}'.\n\tSetting {indices} to {value}"
                )
                record = parameter.add_record(indices)
            else:
                raise ge
        # add_record
        if not apply_percentage and type(value) is not None:
            if isinstance(record, GamsSetRecord):
                # sets only have text i.e. "Y"
                record.set_text(value)
            else:
                record.set_value(value)
        elif apply_percentage:
            current_val = record.get_value()
            record.set_value(current_val * apply_percentage)
        else:
            raise ValueError("one of 'value' and 'apply_percentage' must be passed!")
        return self.gams_db

    def aggregate_timeseries(
        self, export_path, hours_per_period=24 * 7, n_periods=3, investInit_path = None, alternative_investInit_template = None, 
        ts_params = ["ts_influx", "ts_node", "ts_unit", "ts_cf"], err_indicators=None
    ):     
        """use tsam to aggregate time series

        Args:
            export_path (str): path where file with aggregated time series shall be saved (path/to/filename.gdx)
            hours_per_period (int, optional): numbers of hours per period (tsam parameter). Defaults to 24*7.
            n_periods (int, optional): number of representative periods (tsam paramter). Defaults to 3.
            investInit_path (str, optional): path to updated investInit.gms. investInit is only written if this path is given. Defaults to None.
            alternative_investInit_template (str, optional): alternative template for investInit.gms. The following wild cards can be used and will be replaced by the corresponding argument values: "n_periods" and "hours_per_period". Furthermore, the template should contain "    // add sample timesteps", "    // add sample probability", "    // add sample weights" and "    // add sample annuity weights" for insertion of corresponding values. Use method show_investInit_template() to show the default template. Defaults to None.
            ts_params (list, optional): parameters that shall be included in the clustering. Defaults to ["ts_influx", "ts_node", "ts_unit", "ts_cf"].
            err_indicators (str, optional): only "print" or None possible, for debugging. Defaults to None.

        Raises:
            NotImplementedError: if err_indicators is something else but "print" or None
        """        
        # err_indicators="print"|None
        if err_indicators not in ("print", None):
            raise NotImplementedError(
                f" Only one of ('print',None) is supported for `err_indicators`, but {err_indicators=} was passed."
            )

        ts_frames = []
        drop_frames = []
        # retrieve and transform timeseries data (not exaustive)
        for p in ts_params:
            p_df = self.param_as_df_gdxdump(p)
            if p_df.empty:
                drop_frames.append(p)
                continue
            # index of the time column
            time_col = list(p_df.columns).index("t")

            # all the previous columns (time is usually the penultimate column)
            index_cols = list(p_df.columns[:time_col])

            # transform from long to wide dataformat
            p_df = p_df.pivot(index="t", columns=index_cols, values="Val")

            # join column names from different levels and prepend param_name
            # these will come in handy, when writing aggregated data to the *.gdx
            # col is tuple, thus must be converted to a list to be mutable
            p_df.columns = ["|".join([p] + list(col)) for col in p_df.columns]

            ts_frames.append(p_df)
        # merge ts_frames to a single dataframe
        ts_df = reduce(
            lambda left, right: pd.merge(
                left, right, left_index=True, right_index=True, how="outer"
            ),
            ts_frames,
        )

        # create and set a datetimeindex
        dateindex = pd.date_range(start="2020-01-01 00:00", periods=8760, freq="h")
        ts_df.set_index(dateindex, inplace=True)
        ts_df.fillna(0, inplace=True)

        # create aggregation
        aggregation = tsam.TimeSeriesAggregation(
            ts_df,
            hoursPerPeriod=hours_per_period,
            noTypicalPeriods=n_periods,
            clusterMethod="adjacent_periods",
            representationMethod="distributionAndMinMaxRepresentation",
        )

        # calculate the typical periods
        typeriods = aggregation.createTypicalPeriods()

        if err_indicators == "print":
            print(aggregation.accuracyIndicators())

        # get the sequence and number of occurances
        period_sequence = [
            (k, sum(1 for i in g)) for k, g in groupby(aggregation.clusterOrder)
        ]

        # concatenate
        ts_input_data = pd.concat(
            [typeriods.loc[period_no, :] for period_no, _ in period_sequence]
        ).reset_index(drop=True)

        # write data to gdx
        for col_name in ts_input_data.columns:
            # recreate the indices from the column names
            bb_indices = col_name.split("|")

            for i, val in enumerate(ts_input_data[col_name].values):
                timestep = f"t{i + 1:06}"
                self.update_gams_parameter_in_db(
                    bb_indices[0], bb_indices[1:] + [timestep], val
                )

        # add samples to .gdx where nessesary
        samples_and_lengths = [
            {
                "name": f"s{i:03}",
                "length": hours_per_period,
                "weight": tup[1],
                "cluster_no": tup[0],
            }
            for i, tup in enumerate(period_sequence)
        ]
        sample_df = pd.DataFrame.from_records(samples_and_lengths, index="name")
        sample_names = sample_df.index.to_list()

        if "p_s_discountFactor" not in self.input_symbols:
            self.gams_db.add_parameter_dc("p_s_discountFactor", ["s"])
        for sample in sample_df.index:
            self.update_gams_parameter_in_db("p_s_discountFactor", [sample], value=1)
            # : ["sample",	"group"]
            for groupName in self.sgroup()["Dim2"]:
                self.update_gams_parameter_in_db(
                    "sGroup", [sample, groupName], value="Y"
                )

        # bind samples in gnss_bound
        # get nodes that have a state
        p_gn = self.p_gn()
        nodes_w_state = p_gn.query("Dim3=='energyStoredPerUnitOfState'")[
            ["Dim1", "Dim2"]
        ]
        # nodes_w_state.append([nodes_w_state]*(len(sample_names)-1))
        gnss_df = pd.concat([nodes_w_state] * len(sample_names))
        gnss_df.sort_values(by="Dim2", inplace=True)

        from_sample = []
        to_sample = []
        for i in range(len(gnss_df)):
            from_sample.append(sample_names[i % len(sample_names)])
            to_sample.append(sample_names[(i + 1) % len(sample_names)])

        gnss_df["from_sample"] = from_sample
        gnss_df["to_sample"] = to_sample

        # clear records in bounds, because they might be invalid post-aggregation
        gnss_bounds = self.gams_db.get_symbol("gnss_bound")
        gnss_bounds.clear()

        for gnss_indices in gnss_df.values:
            # print(gnss_indices)
            self.update_gams_parameter_in_db(
                "gnss_bound", list(gnss_indices), value="Y"
            )

        if investInit_path == None:
            print("Dont forget to update your bb input configuration!!")
            for i, tup in enumerate(period_sequence):
                print(
                    f"s{i:03} - cluster:{tup[0]} - weight:{tup[1]},\tlength: {hours_per_period}"
                )
        else:
            investInit = self.investInit_for_aggregatedTimeseries(hours_per_period, n_periods, sample_df["weight"].to_list(), alternative_investInit_template)
            with open((investInit_path), "w") as f:
                f.write(investInit)
        
        sample_df.to_csv(str(export_path) + "_sample_weights.csv")
        self.gams_db.export(export_path)
        pass

    def investInit_for_aggregatedTimeseries(self, hours_per_period, n_periods, weights, alternative_investInit_template = None):
        """creates new investInit for aggregated timeseries

        Args:
            hours_per_period (int, optional): numbers of hours per period (tsam parameter). Defaults to 24*7.
            n_periods (int, optional): number of representative periods (tsam paramter). Defaults to 3.
            weights (list): list of weights for sample
            alternative_investInit_template (str, optional): alternative template for investInit.gms. The following wild cards can be used and will be replaced by the corresponding argument values: "n_periods" and "hours_per_period". Furthermore, the template should contain "    // add sample timesteps", "    // add sample probability", "    // add sample weights" and "    // add sample annuity weights" for insertion of corresponding values. Use method show_investInit_template() to show the default template. Defaults to None.

        Returns:
            str: new investInit
        """        
        if alternative_investInit_template == None:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "investInit_template.gms"), "r") as f:
                filedata = f.read()
        else:
            with open(alternative_investInit_template, "r") as f:
                filedata = f.read()

        newdata = filedata.replace("hours_per_period", str(hours_per_period))
        newdata = newdata.replace("n_periods", str(n_periods))
        sample_string = ""
        probability_string = ""
        weight_string = ""
        annuityWeight_string = ""

        for i, weight in enumerate(weights):
            if i == 0:  
                sample_string = sample_string+f"\tmsStart('invest', 's{i:03d}') = 1;\n\tmsEnd('invest', 's{i:03d}') = msStart('invest', 's{i:03d}') + {hours_per_period};\n"
            else:
                sample_string = sample_string+f"\tmsStart('invest', 's{i:03d}') = msEnd('invest', 's{i-1:03d}');\n\tmsEnd('invest', 's{i:03d}') = msStart('invest', 's{i:03d}') + {hours_per_period};\n"
            probability_string = probability_string + f"\tp_msProbability('invest', 's{i:03d}') = 1;\n"
            weight_string = weight_string + f"\tp_msWeight('invest', 's{i:03d}') = {weight};\n"
            annuityWeight_string = annuityWeight_string + f"    p_msAnnuityWeight('invest', 's{i:03d}') = {hours_per_period*weight}/8760;\n"

        newdata = newdata.replace("    // add sample timesteps", sample_string)
        newdata = newdata.replace("    // add sample probability", probability_string)
        newdata = newdata.replace("    // add sample weights", weight_string)
        newdata = newdata.replace("    // add sample annuity weights", annuityWeight_string)

        return newdata
    
    def show_investInit_template(self):
        """Shows investInit.gms template to simplify building own template
        """        
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "investInit_template.gms"), "r") as f:
            filedata = f.read()
        print(filedata)