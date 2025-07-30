# observe-sdk

An Airflow and Python SDK for working with the Astro Observe platform

## Installation

Add the following to your `requirements.txt`:

```text
astro-observe-sdk==0.0.1
```

## Usage

### Metrics

The Observe SDK allows you to emit metrics during Airflow task execution to get tracked in the Observe backend. To do so, use the `astro_observe_sdk.log_metric` function like so:

```python
import astro_observe_sdk as observe

# then, in your task
@task
def my_task():
    observe.log_metric('my_metric', 42)
```
