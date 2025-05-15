from dagster import Definitions
import dagster_jaffle_shop.defs

from dagster.components import definitions, load_defs


@definitions
def defs() -> Definitions:
    return load_defs(defs_root=dagster_jaffle_shop.defs)
