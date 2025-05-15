import os
from dagster_azure.adls2 import ADLS2Resource, ADLS2SASToken
from dagster_dbt import DbtCliResource
from dagster_duckdb import DuckDBResource
import dagster as dg


defs = dg.Definitions(
    resources={},
)
