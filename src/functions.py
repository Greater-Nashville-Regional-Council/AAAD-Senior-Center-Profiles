import sqlite3 as sq

import pandas as pd

from src.paths import CENSUS_DB

def read_census_table(
    table_name,
    geographies=None,
    columns=None,
    geography_col="NAME",
    merge_on="GEO_ID"
):
    """Read and merge horizontally split Census tables from SQLite.

    Parameters
    ----------
    table_name : str
        Base table name, e.g. ACS5_2024.
    geographies : list, optional
        Values used to filter the geography column.
        If None, returns all geographies.
    columns : list, optional
        Columns to return. If None, returns all columns.
    geography_col : str, default "NAME"
        Column used to filter geographies.
    merge_on : str, default "GEO_ID"
        Unique identifier used to merge split tables.

    Returns
    -------
    pandas.DataFrame
        Combined Census data.
    """

    with sq.connect(CENSUS_DB) as conn:

        #find matching tables
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type = 'table'",
            conn
        )["name"].tolist()

        if table_name in tables:
            matching_tables = [table_name]
        else:
            matching_tables = sorted(
                [
                    t for t in tables
                    if t.startswith(f"{table_name}_")
                    and t.rsplit("_", 1)[-1].isdigit()
                ],
                key=lambda t: int(t.rsplit("_", 1)[-1])
            )

        if not matching_tables:
            raise ValueError(f"No tables found for {table_name}")

        #get columns for each table
        table_cols = {}

        for table in matching_tables:
            table_cols[table] = [
                row[1]
                for row in conn.execute(
                    f'PRAGMA table_info("{table}")'
                )
            ]

        #check requested columns
        available_all = set().union(
            *(set(cols) for cols in table_cols.values())
        )

        if columns is not None:
            missing = set(columns) - available_all
            if missing:
                raise ValueError(f"Columns not found: {missing}")

        dfs = []

        for table in matching_tables:

            available = table_cols[table]

            if merge_on not in available:
                raise ValueError(f"{merge_on} not found in {table}")

            if geographies is not None and geography_col not in available:
                raise ValueError(f"{geography_col} not found in {table}")

            if columns is None:
                selected = available.copy()
            else:
                selected = [
                    col for col in columns if col in available
                ]

                #always include merge key
                if merge_on not in selected:
                    selected.insert(0, merge_on)

                #skip tables without requested non-key columns
                if not any(col != merge_on for col in selected):
                    continue

            select_sql = ", ".join(
                f'"{col}"' for col in selected
            )

            query = f'SELECT {select_sql} FROM "{table}"'
            params = []

            if geographies is not None:
                if not geographies:
                    return pd.DataFrame(columns=columns)

                placeholders = ", ".join(
                    "?" for _ in geographies
                )

                query += (
                    f' WHERE "{geography_col}" IN ({placeholders})'
                )

                params = geographies

            df = pd.read_sql_query(query, conn, params=params)

            if df.duplicated(subset=[merge_on]).any():
                raise ValueError(f"Duplicate {merge_on} values in {table}")

            dfs.append(df)

    if not dfs:
        return pd.DataFrame(columns=columns)

    #merge tables
    result = dfs[0]

    for df in dfs[1:]:

        #remove duplicate non-key columns
        overlapping = [
            col for col in df.columns
            if col in result.columns and col != merge_on
        ]

        df = df.drop(columns=overlapping)

        result = result.merge(
            df,
            on=merge_on,
            how="inner",
            validate="one_to_one"
        )

    #return requested columns
    if columns is not None:
        result = result[columns]

    return result.reset_index(drop=True)