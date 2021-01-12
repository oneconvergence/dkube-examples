import json
import random
import os
import click

import pandas as pd


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path(exists=True))
def eval(input_file, output_dir):
    """Eval script which compares prediction with ground truth."""
    predictions = pd.read_csv(input_file, index_col="PassengerId")
    dirpath = os.path.dirname(os.path.abspath(__file__))
    ground_truth = pd.read_csv(dirpath + "/ground_truth.csv", index_col="PassengerId")

    accurate = (predictions["Survived"] == ground_truth["Survived"]).cumsum().tolist()
    accuracy = accurate[-1] * 100 / len(predictions)

    metrics = {
        "metrics": [{"accuracy": accuracy}, {"loss": random.random()}],
        "sort": "accuracy",
    }
    with open(output_dir + "/metrics.json", "w") as f:
        json.dump(metrics, f)
    print(f"Accuracy: {round(accuracy,2)}")


if __name__ == "__main__":
    eval()