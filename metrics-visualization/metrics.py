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
    roc = [
        [1.0, 0.635165,0.0], 
        [1.0, 0.766586,1.0], 
        [1.0, 0.724564,1.0],
        [1.0, 0.766586,1.0],
        [1.0, 0.889199,1.0],
        [1.0, 0.966586,1.0],
        [1.0, 0.535165,0.0],
        [1.0, 0.55165,0.0],
        [1.0, 0.525165,0.0],
        [1.0, 0.5595165,0.0] ]
    df_roc = pd.DataFrame(roc,columns = ['fpr','tpr','thresholds'])
    

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
            'storage': 'inline',
            'source': df_roc.to_csv(header=False, index=False)
            },
            {
            "storage": "inline",
            "type": "table",
            "format": "csv",
            "header": ["cv_accuracy", "cv_brier_score"],
            "source": "0.78, 0.88",
            }
        ]
    }

    with open("/output/metrics.json", "w") as f:
        json.dump(metadata, f)
    accuracy = 70
    metrics = {
    'metrics': [{
      'name': 'accuracy-score', # The name of the metric. Visualized as the column name in the runs table.
      'numberValue':  accuracy, # The value of the metric. Must be a numeric value.
      'format': "PERCENTAGE",   # The optional format of the metric. Supported values are "RAW" (displayed in raw format) and "PERCENTAGE" (displayed in percentage format).
    }]
  }
    with open("/output/mlpipeline-metrics.json", "w") as f:
        json.dump(metadata, f)


produce_metrics()

