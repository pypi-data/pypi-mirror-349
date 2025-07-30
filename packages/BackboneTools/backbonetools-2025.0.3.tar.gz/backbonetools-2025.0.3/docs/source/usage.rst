Usage
=====

.. _installation:

Installation
------------

An important prerequisite is to have [GAMS](https://www.gams.com/) installed on your system, as this packages calls certain GAMS commands through python.
To use BackboneTools, install it using pip:

.. code-block:: console

   (.venv) $ pip install backbonetools

Example of usage
------------

.. code-block:: python

   from backbonetools.io import BackboneResult 

   result = BackboneResult('someBackboneOutputFile.gdx')

   # any symbol is available as DataFrame
   gen_df = result.r_gen_gnuft()
   gen_df.head()

This yields something like this:

+----+-------+--------+---------------+-----+----+--------+
|    | grid  | node   | unit          | f   | t  | Val    |
+====+=======+========+===============+=====+====+========+
|  0 | elec  | AT0 0  | AT0 0 CCGT    | f00 | 6  | 3295.9 |
+----+-------+--------+---------------+-----+----+--------+
|  1 | elec  | AT0 0  | AT0 0 CCGT    | f00 | 7  | 3295.9 |
+----+-------+--------+---------------+-----+----+--------+
|  2 | elec  | AT0 0  | AT0 0 CCGT    | f00 | 8  | 3295.9 |
+----+-------+--------+---------------+-----+----+--------+
|  3 | elec  | AT0 0  | AT0 0 CCGT    | f00 | 9  | 3295.9 |
+----+-------+--------+---------------+-----+----+--------+
|  4 | elec  | AT0 0  | AT0 0 CCGT    | f00 | 10 | 3295.9 |
+----+-------+--------+---------------+-----+----+--------+

More detailed explanations of the exisiting functionallities can be found in the :ref:`API` description.