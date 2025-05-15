import io
import dagster as dg
from dagster_azure.adls2 import ADLS2Resource
from dagster_duckdb import DuckDBResource
import pandas as pd

container_name = "jaffle-shop"


def read_blob_from_adls2(adls2: ADLS2Resource, blob_name: str) -> pd.DataFrame:
    blob_client = adls2.blob_client.get_blob_client(
        container=container_name, blob=blob_name
    )
    csv_bytes = blob_client.download_blob().readall()
    return pd.read_csv(io.BytesIO(csv_bytes))


def load_data(
    table_name: str, blob_name: str, adls2: ADLS2Resource, duckdb: DuckDBResource
) -> dg.MaterializeResult:
    df = read_blob_from_adls2(adls2, blob_name)

    with duckdb.get_connection() as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
        conn.execute(f"DROP TABLE IF EXISTS raw.{table_name}")
        conn.execute(f"CREATE TABLE raw.{table_name} AS SELECT * FROM df")

    return dg.MaterializeResult(
        metadata={
            "dagster/uri": f"abfss://{container_name}@{adls2.adls2_client.account_name}.dfs.core.windows.net/{blob_name}",
            "dagster/row_count": len(df),
            "dagster/columns": list(df.columns),
        }
    )
