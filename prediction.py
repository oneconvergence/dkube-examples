import os

import mlflow.sklearn
from sklearn import metrics
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

import utils


class TreeModel:
    """
    DecisionTree classifier to predict binary labels(malignant and benign) of  cancer dataset.
    """

    def __init__(self, **model_params):
        """
        Constructor
        :param model_params: parameters (key-value) for the tree model such as no of estimators, depth of the tree, random_state etc
        """
        self._decision_tree = DecisionTreeClassifier(**model_params)
        self._params = model_params
        self.data = load_breast_cancer()

    @classmethod
    def create_instance(cls, **model_params):
        return cls(**model_params)

    @property
    def model(self):
        """
        Getter for the property the model
        :return: return the trained decision tree model
        """

        return self._decision_tree

    @property
    def params(self):
        """
        Getter for the property the model
          :return: return the model params
        """
        return self._params

    def mlflow_run(self, run_name="Breast Cancer Classification Run"):
        """
        This method trains, computes metrics, and logs all metrics, parameters,
        and artifacts for the current run
        :param run_name: Name of the experiment as logged by MLflow
        :return: MLflow Tuple (experiment_id, run_id)
        """

        with mlflow.start_run(run_name=run_name) as run:

            # get current run and experiment id
            run_id = run.info.run_uuid
            experiment_id = run.info.experiment_id

            # split the data into train and test
            X_train, X_test, y_train, y_test = train_test_split(self.data.data,
                                                                self.data.target,
                                                                test_size=0.25,
                                                                random_state=23)

            # train and predict
            self._decision_tree.fit(X_train, y_train)
            y_pred = self._decision_tree.predict(X_test)
            y_probs = self._decision_tree.predict_proba(X_test)

            # Log model and params using the MLflow sklearn APIs
            mlflow.sklearn.log_model(self.model, "decision-tree-classifier")
            mlflow.log_params(self.params)

            acc = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            conf_matrix = confusion_matrix(y_test, y_pred)

            roc = metrics.roc_auc_score(y_test, y_pred)

            # confusion matrix values
            tp = conf_matrix[0][0]
            tn = conf_matrix[1][1]
            fp = conf_matrix[0][1]
            fn = conf_matrix[1][0]

            # get classification metrics
            class_report = classification_report(y_test, y_pred, output_dict=True)
            recall_0 = class_report['0']['recall']
            f1_score_0 = class_report['0']['f1-score']
            recall_1 = class_report['1']['recall']
            f1_score_1 = class_report['1']['f1-score']

            # log metrics in mlflow
            mlflow.log_metric("accuracy_score", acc)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("true_positive", tp)
            mlflow.log_metric("true_negative", tn)
            mlflow.log_metric("false_positive", fp)
            mlflow.log_metric("false_negative", fn)
            mlflow.log_metric("recall_0", recall_0)
            mlflow.log_metric("f1_score_0", f1_score_0)
            mlflow.log_metric("recall_1", recall_1)
            mlflow.log_metric("f1_score_1", f1_score_1)
            mlflow.log_metric("roc", roc)

            # create confusion matrix plot
            plt_cm, fig_cm, ax_cm = utils.plot_confusion_matrix(y_test, y_pred, y_test,
                                                                title="Classification Confusion Matrix")

            temp_name = "confusion-matrix.png"
            fig_cm.savefig(temp_name)
            mlflow.log_artifact(temp_name, "confusion-matrix-plots")
            try:
                os.remove(temp_name)
            except FileNotFoundError as e:
                print(f"{temp_name} file is not found")

            # create roc plot
            plot_file = "roc-auc-plot.png"
            probs = y_probs[:, 1]
            fpr, tpr, thresholds = roc_curve(y_test, probs)
            plt_roc, fig_roc, ax_roc = utils.create_roc_plot(fpr, tpr)
            fig_roc.savefig(plot_file)
            mlflow.log_artifact(plot_file, "roc-auc-plots")
            try:
                os.remove(plot_file)
            except FileNotFoundError as e:
                print(f"{temp_name} file is not found")

            print("<->" * 40)
            print("Inside MLflow Run with run_id {run_id} and experiment_id {experiment_id}")
            print("max_depth of trees:", self.params["max_depth"])
            print(conf_matrix)
            print(classification_report(y_test, y_pred))
            print("Accuracy Score =>", acc)
            print("Precision      =>", precision)
            print("ROC            =>", roc)

            return experiment_id, run_id
