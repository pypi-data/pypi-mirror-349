"Utilities for the astro_observe_sdk package."

import os
from airflow import __version__

if __version__ >= "3.0.0":
    from airflow.sdk import get_current_context
else:
    from airflow.operators.python import get_current_context
from airflow.providers.openlineage.plugins.macros import lineage_run_id


def generate_asset_id():
    "Uses the current task context to generate an asset ID."
    task_instance = get_current_context().get("task_instance")

    if not task_instance:
        raise ValueError(
            "Task context not found. Please run this function within an Airflow task."
        )

    namespace = os.getenv("ASTRO_DEPLOYMENT_NAMESPACE")
    dag_id = task_instance.dag_id
    task_id = task_instance.task_id

    asset_id = f"{namespace}.{dag_id}.{task_id}"
    return asset_id


def get_lineage_run_id():
    "Uses the current task context to get a lineage run ID."
    task_instance = get_current_context().get("task_instance")

    if not task_instance:
        raise ValueError(
            "Task context not found. Please run this function within an Airflow task."
        )

    return lineage_run_id(task_instance)
