from typing import Any

import duckdb
import mcpf_core.core.routines as routines
from mcpf_core.func import constants


def df_sql_statement(data: dict[str, Any]) -> dict[str, Any]:
    """Executes a SQL query on a given pandas DataFrame and returns the transformed DataFrame.

    This function reads a pandas DataFrame (`df`) and a SQL query (`query`), applies the SQL query
    on the DataFrame, and returns a new DataFrame containing the results of the query.

    Args:
        data (dict[str, Any]): _description_

    Returns:
        dict[str, Any]: _description_
    """
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {"input": constants.DEFAULT_IO_DATA_LABEL, "output": constants.DEFAULT_IO_DATA_LABEL, "query": ""}
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg["input"] = iterator

    # create DuckDB connection
    conn = duckdb.connect(database=":memory:")
    conn.register("data", data[arg["input"]])

    query = arg["SQL_STMT"] if not arg["query"] and "SQL_STMT" in arg else arg["query"]

    df = conn.execute(query).fetchdf()

    data[arg["output"]] = df
    routines.set_meta_in_data(data, meta)
    return data
