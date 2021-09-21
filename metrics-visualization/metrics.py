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
    df_roc = pd.DataFrame({'fpr': fpr, 'tpr': tpr, 'thresholds': thresholds})
    roc_file = '/output/roc.csv'
    with open(roc_file, 'w') as f:
        df_roc.to_csv(f, columns=['fpr', 'tpr', 'thresholds'], header=False, index=False)

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
            },
            {
            'type': 'roc',
            'format': 'csv',
            'schema': [
                {'name': 'fpr', 'type': 'NUMBER'},
                {'name': 'tpr', 'type': 'NUMBER'},
                {'name': 'thresholds', 'type': 'NUMBER'},
            ],
            'source': roc_file
            }
        ]
    }

    with open("/output/metrics.json", "w") as f:
        json.dump(metadata, f)
    accuracy_score = 0.6
    roc_auc_score = 0.75
    metrics = {
        'metrics': [
            {
                'name': 'accuracy-score',
                'numberValue':  accuracy_score,
                'format': 'PERCENTAGE'
            },
            {
                'name': 'roc-auc-score',
                'numberValue':  roc_auc_score,
                'format': 'RAW'       
            }
        ]
    }
    with open('/output/mlpipeline-metrics.json', 'w') as f:
        json.dump(metrics, f)


produce_metrics()

