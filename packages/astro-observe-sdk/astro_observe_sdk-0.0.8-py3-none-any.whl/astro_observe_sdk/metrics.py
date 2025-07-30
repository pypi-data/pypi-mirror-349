"User-facing methods to interact with the Metrics API"

import os
from typing import Unpack

import pendulum

from astro_observe_sdk.clients.config import TypedCommonConfig
from astro_observe_sdk.clients.metrics import Metric, MetricCategory
from astro_observe_sdk.clients.metrics import log_metric as _log_metric

from astro_observe_sdk.utils import generate_asset_id, get_lineage_run_id


def log_metric(
    name: str,
    value: float,
    asset_id: str | None = None,
    timestamp: pendulum.DateTime | None = None,
    **kwargs: Unpack[TypedCommonConfig],
) -> None:
    """
    Log a single metric to the Metrics API. Automatically pulls in task context.
    """
    deployment_id = os.getenv("ASTRO_DEPLOYMENT_ID")
    if not deployment_id:
        raise ValueError(
            "Deployment ID not found. This should be automatically set by Astro."
        )

    asset_id = generate_asset_id() if not asset_id else asset_id
    run_id = get_lineage_run_id()

    metric = Metric(
        asset_id=asset_id,
        deployment_id=deployment_id,
        run_id=run_id,
        category=MetricCategory.CUSTOM,
        name=name,
        value=value,
        timestamp=timestamp,
    )

    _log_metric(metric, **kwargs)
