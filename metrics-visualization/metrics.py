import json
import pandas as pd

def produce_metrics():
    matrix = [
        ['yummy', 'yummy', 10],
        ['yummy', 'not yummy', 2],
        ['not yummy', 'yummy', 6],
        ['not yummy', 'not yummy', 7]
    ]

    df = pd.DataFrame(matrix,columns=['target','predicted','count'])

    metadata = {
        "outputs": [
            {
                "type": "confusion_matrix",
                "format": "csv",
                "schema": [
                    {
                        "name": "target",
                        "type": "CATEGORY"
                    },
                    {
                        "name": "predicted",
                        "type": "CATEGORY"
                    },
                    {
                        "name": "count",
                        "type": "NUMBER"
                    }
                ],
                "source": df.to_csv(header=False, index=False),
                "storage": "inline",
                "labels": [
                    "yummy",
                    "not yummy"
                ]
            }
        ]
    }

    with open("/output/metrics.json", "w") as f:
        json.dump(metadata, f)


produce_metrics()

