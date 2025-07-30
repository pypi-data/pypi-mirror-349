"""contains execution helpers like a function to run backbone via python
or automated scenario analysis
"""

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

import os
import subprocess as sp
from glob import glob
from multiprocessing.pool import ThreadPool
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook

from backbonetools.io.inputs import BackboneInput
from backbonetools.io.outputs import BackboneResult


def run_backbone(
    backbone_dir,
    input_dir,
    input_file_gdx,
    output_dir,
    output_file=None,
    **kwargs,
):
    """runs Backbone with the specified arguments

    Args:
        backbone_dir (str): Path to the Backbone Framework.
        input_dir (str): Path to the input directory for Backbone to read configurations (e.g. `investInit.gms`)
        input_file_gdx (str): Path to the Backbone input file
        output_dir (str): Path to the output directory, where results shall be written
        output_file (str): Name of the Backbone result file

    Raises:
        ValueError: if any path contains spaces, an error occurs

    Returns:
        str: path to output file
    """    

    # if not specified, derive from input_file_gdx
    if not output_file:
        output_file = Path(input_file_gdx).stem + "_result.gdx"

    # if not specified, set backbone_dir to submodule path
    if not backbone_dir:
        backbone_dir = Path(__file__).parent.parent.joinpath("backbone")

    # keyword arguments are parsed into backbone suitable form
    # e.g. dict(maxTotalCost=42) will be passed as "--maxTotalCost=42" to backbone
    keyword_args = [f"--{k}={v}" for k, v in kwargs.items()]

    # spaces in file names don't work through subprocesses
    contain_spaces = [
        " " in str(file_or_dir)
        for file_or_dir in [input_dir, input_file_gdx, output_dir, output_file]
    ]
    if any(contain_spaces):
        raise ValueError(
            "Passing paths with spaces via subprocess to Gams is not supported yet."
        )

    # absolute paths are better for gams
    input_dir = Path(input_dir).absolute().as_posix()
    input_file_gdx = Path(input_file_gdx).absolute().as_posix()
    output_dir = Path(output_dir).absolute().as_posix()

    Path(input_dir).mkdir(exist_ok=True)
    Path(output_dir).mkdir(exist_ok=True)

    process_output = sp.run(
        [
            "gams",
            "Backbone.gms",
            f"--input_dir={input_dir}",
            f"--input_file_gdx={input_file_gdx}",
            f"--output_dir={output_dir}",
            f"--output_file={output_file}",
            *keyword_args,
        ],
        cwd=backbone_dir,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        # text= True
    )

    # stdout, stderr = process_output.communicate()
    # write terminal output to a file
    open(f"{output_dir}/{Path(output_file).stem}_terminal.log", "w").write(
        process_output.stdout.decode()
    )
    open(f"{output_dir}/{Path(output_file).stem}_error.log", "w").write(
        process_output.stderr.decode()
    )
    print("finished", output_file)
    return Path(output_dir).joinpath(output_file).absolute()


def sensitivity(
    input_file_gdx,
    bb_input_dir,
    output_dir=None,
    parallel=True,
    param="CO2",
    percentages=[0.05, 0.1, 0.2, 0.4, 0.8],
):
    """Runs sensitivity analysis with a given input file, varying one parameter over certain values

    Args:
        input_file_gdx (str): path to original input data file (.gdx)
        bb_input_dir (str): path to backbone input dir (contains e.g. investInit.gms)
        output_dir (str, optional): path to outputdir. Defaults to None.
        parallel (bool, optional): If backbone shall be run in parallel for the different scenarios. Defaults to True.
        param (str, optional): parameter to be varied. Defaults to "CO2". At the moment, only CO2 is implemented
        percentages (list, optional): values for parameter, as a share of the value the parameter has when running the original input file. Defaults to [0.05, 0.1, 0.2, 0.4, 0.8].

    Raises:
        NotImplementedError: rises exception if no sensitivity analysis for the used parameter is implemented

    Returns:
        list: path to result gdx files
    """
    if param != "CO2":
        raise NotImplementedError(
            f"sensitivity not yet implemented for parameters other than {param}."
        )

    sensitivity_dir = Path(input_file_gdx).parent
    sensitivity_input_dir = f"{sensitivity_dir}/{param}_inputs"
    if not output_dir:
        sensitivity_output_dir = f"{sensitivity_dir}/{param}_outputs"
    else:
        sensitivity_output_dir = output_dir

    # create directories
    Path(sensitivity_input_dir).mkdir(exist_ok=True)
    Path(sensitivity_output_dir).mkdir(exist_ok=True)

    bb_in = BackboneInput(input_file_gdx)
    bb_opt_fn = bb_in._path.stem + f"_100{param}_result.gdx"

    # run first optimisation i.e. 100% of `param`
    bb_out_path = run_backbone(
        bb_input_dir,
        input_file_gdx=bb_in._path,
        output_dir=sensitivity_output_dir,
        output_file=bb_opt_fn,
    )

    # from scripts.results import BackboneResult
    bb_result = BackboneResult(bb_out_path)
    bb_result.r_emission()

    emission_lims = bb_result.r_emission()["Val"].values * percentages
    # percentages,emission_lims

    for percentage, em_lim in zip(percentages, emission_lims):
        new_db = bb_in.update_gams_parameter_in_db(
            "p_groupPolicyEmission",
            ["emission group", "emissionCap", "CO2"],
            value=em_lim,
        )
        out_fn = Path(bb_in._path).stem + f"_{percentage*100:02.0f}{param}"
        Path(sensitivity_input_dir).mkdir(exist_ok=True)
        new_db.export(f"{sensitivity_input_dir}/{out_fn}.gdx")

    input_files = list(glob(f"{sensitivity_input_dir}/*.gdx"))
    result_paths = []

    if parallel:
        threads = os.cpu_count() - 1
        with ThreadPool(threads) as pool:
            jobs = []
            for file in input_files:
                job = pool.apply_async(
                    run_backbone, (bb_input_dir, file, sensitivity_output_dir)
                )
                jobs.append(job)
            result_paths = [job.get() for job in jobs]
    else:
        for file in input_files:
            path = run_backbone(bb_input_dir, file, sensitivity_output_dir)
            result_paths.append(path)

    return result_paths

def invest2schedule(input_xlsx, result_gdx, schedule_xlsx_path=None):
    """_summary_

    Args:
        input_xlsx (str): path to input data with complete time series and other data (like p_gnu_io) the same as used for invest run
        result_gdx (str): path to investment result
        schedule_xlsx_path (str, optional): Path to output xlsx. Defaults to None.

    Returns:
        str: path to output xlsx
    """
    # # Invest 2 Schedule
    # ### read an investment result and its' input file, create a new input file

    bb_input_path = input_xlsx
    bb_output_path = result_gdx

    if schedule_xlsx_path is None:
        schedule_xlsx_path = Path(bb_input_path).stem + "_schedule.xlsx"
        schedule_xlsx_path = Path(bb_input_path).parent.joinpath(schedule_xlsx_path)

    result = BackboneResult(bb_output_path)
    invested_capacities = result.r_invest_unitCapacity_gnu().dropna()

    wb = load_workbook(bb_input_path)
    p_gnu_io = wb["p_gnu_io"]
    p_gnu_io_values = list(p_gnu_io.values)
    p_gnu_io_df = pd.DataFrame(p_gnu_io_values[1:], columns=p_gnu_io_values[0])

    # we only put cost data, where input/output == "output"
    idx_output = p_gnu_io_df["input output"] == "output"

    output_df = p_gnu_io_df.loc[idx_output, :]
    int_idx = invested_capacities["unit"].apply(
        lambda x: output_df.index[output_df["unit"] == x][0]
    )

    # add investments to previously existing
    invest_rows = output_df.loc[int_idx, :]

    # replace eps with 0 to enable addition
    invest_rows = invest_rows.replace("eps", 0)
    invest_rows["capacity"] += invested_capacities["Val"].values

    # replace 0 with eps for backbone
    invest_rows = invest_rows.replace(0, "eps")

    # overwrite values in p_gnu_io frame
    # note that index of p_gnu_io_df and output_df is consistent
    p_gnu_io_df.loc[int_idx, "capacity"] = invest_rows["capacity"]

    p_gnu_io.delete_rows(idx=2, amount=9999)
    for tup in p_gnu_io_df.itertuples(index=False):
        # bb_indices = col_name.split("|")
        p_gnu_io.append([*tup])

    # disable investments: set max unit count to 0
    p_unit = wb["p_unit"]
    p_unit_values = list(p_unit.values)
    p_unit_df = pd.DataFrame(p_unit_values[1:], columns=p_unit_values[0])
    p_unit_df["maxUnitCount"] = 0

    p_unit.delete_rows(idx=2, amount=9999)
    for tup in p_unit_df.itertuples(index=False):
        p_unit.append([*tup])

    # Calculate new upper bounds for storages

    storage_investments = invested_capacities.query("grid == 'storage'")

    # get upperLimitCapacityRatio from p_gnu_io
    upperLimitCapacityRatio = p_gnu_io_df.set_index(["grid", "node", "unit"])["upperLimitCapacityRatio"]
    # calculate new upperBound
    upperBound_df = pd.merge(storage_investments.set_index(["grid", "node", "unit"]), upperLimitCapacityRatio, how ="left", left_index=True, right_index=True)
    upperBound_df["constant"] = upperBound_df["Val"]*upperBound_df["upperLimitCapacityRatio"]
    upperBound_df["param_gnBoundaryTypes"] = "upwardLimit"
    upperBound_df["useConstant"] = 1
    upperBound_df["useTimeseries"] = 0
    upperBound_df = upperBound_df.loc[upperBound_df["constant"] != 0].groupby(["grid", "node", "param_gnBoundaryTypes", "useConstant", "constant", "useTimeseries"]).sum().reset_index()[["grid", "node", "param_gnBoundaryTypes", "useConstant", "constant", "useTimeseries"]]

    # add to exisiting upward limits
    p_gnBoundaryPropertiesForStates = wb["p_gnBoundaryPropertiesForStates"]
    p_gnBoundaryPropertiesForStates_values = list(p_gnBoundaryPropertiesForStates.values)
    p_gnBoundaryPropertiesForStates_df = pd.DataFrame(p_gnBoundaryPropertiesForStates_values[1:], columns=p_gnBoundaryPropertiesForStates_values[0])
    p_gnBoundaryPropertiesForStates_df.set_index(["grid", "node", "param_gnBoundaryTypes", "useConstant", "useTimeseries"], inplace=True)
    
    p_gnBoundaryPropertiesForStates_df = p_gnBoundaryPropertiesForStates_df.add(upperBound_df.set_index(["grid", "node", "param_gnBoundaryTypes", "useConstant", "useTimeseries"]), fill_value=0)
    p_gnBoundaryPropertiesForStates_df = p_gnBoundaryPropertiesForStates_df.reset_index()[["grid", "node", "param_gnBoundaryTypes", "useConstant", "constant", "useTimeseries"]]

    # overwrite values in p_gnBoundaryPropertiesForStates frame
    p_gnBoundaryPropertiesForStates.delete_rows(idx=2, amount=9999)
    for tup in p_gnBoundaryPropertiesForStates_df.itertuples(index=False):
        p_gnBoundaryPropertiesForStates.append([*tup])

    # add investments in p_gnn
    grid_investments = result.r_invest_transferCapacity_gnn()
    # handle different GAMS versions
    try:
        grid_investments = grid_investments.set_index(["grid", "node", "node.1"])
    except:
        grid_investments = grid_investments.set_index(["grid", "node", "node_1"])

    p_gnn_sheet = wb["p_gnn"]
    p_gnn_values = list(p_gnn_sheet.values)
    p_gnn_df = pd.DataFrame(p_gnn_values[1:], columns=p_gnn_values[0])

    # update index to enable easy merging of values
    p_gnn_df = p_gnn_df.set_index(["grid", "from node", "to node"])
    p_gnn_df.loc[grid_investments.index, "transferCap"] += grid_investments["Val"]

    # disable further investments
    p_gnn_df["transferCapInvLimit"] = "eps"

    # overwrite the sheet with updated values
    p_gnn_sheet.delete_rows(idx=2, amount=9999)
    p_gnn_df = p_gnn_df.reset_index()
    for tup in p_gnn_df.itertuples(index=False):
        p_gnn_sheet.append([*tup])

    wb.save(schedule_xlsx_path)
    return schedule_xlsx_path
