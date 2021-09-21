import json


def produce_metrics():
    accuracy = 0.9
    metrics = {
        "metrics": [
            {
                "name": "accuracy-score",  # The name of the metric. Visualized as the column name in the runs table.
                "numberValue": accuracy,  # The value of the metric. Must be a numeric value.
                "format": "PERCENTAGE",  # The optional format of the metric. Supported values are "RAW" (displayed in raw format) and "PERCENTAGE" (displayed in percentage format).
            }
        ]
    }
    with open("/output/metrics.json", "w") as f:
        json.dump(metrics, f)


produce_metrics()

