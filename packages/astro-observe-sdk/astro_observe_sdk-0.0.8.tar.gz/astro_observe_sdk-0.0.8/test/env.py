import os
import pytest
from unittest import mock


@pytest.fixture
def setup_env():
    with mock.patch.dict(
        os.environ,
        {
            "ASTRO_DEPLOYMENT_ID": "test-deployment-id",
            "ASTRO_DEPLOYMENT_NAMESPACE": "test-deployment-namespace",
            "ASTRO_ORGANIZATION_ID": "test-org-id",
            "OBSERVE_API_TOKEN": "test-api-token",
        },
    ):
        yield
