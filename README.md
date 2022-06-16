This branch contains examples for monitoring a deployment. A deployment could be an inference service deployed on local DKube or external SageMaker/DKube clusters. The examples showcase Deployment service monitoring (Health of a deployment) as well as model drift and performance monitoring. For model monitoring, we support classification and regression models for tabular or image data. 

### Model Monitoring Examples

- [insurance_datasources](insurance_datasources) - this example demonstrates on how to monitor a imported/deployed regression model in Dkube, where the predict data source can be **local, SQL or AWS S3**. In this example, there is no real deployment to monitor. Data is generated for simulation purposes.
- [insurance_cloudevents](insurance_cloudevents) - this example demonstrates on how to monitor a model when the model is deployed with in DKube with logs enabled and predict data source is **cloudevent logs**. The reference model is a Regression model for insurance application which takes tabular input data.
- [insurance_sagemaker](insurance_sagemaker) - this example demonstrates on how to monitor a model when the model is deployed in AWS Sagemaker with logs enabled and predict data source is **Sagemaker logs**. The reference model is a Regression model for insurance application which takes tabular input data.
- [titanic_datasources](titanic_datasources) - this example demonstrates on how to monitor a imported/deployed classification model in Dkube, where the predict data source can be **local, SQL or AWS S3**. In this example, there is no real deployment to monitor. Data is generated for simulation purposes.
- [image_cloudevents](image_cloudevents) - this example demonstrates on how to monitor a model when the model is deployed with in DKube with logs enabled and predict data source is **cloudevent logs**. The reference model is a Classification model for Chest X-Ray application which takes X-Ray images input data.
- [image_sagemaker](image_sagemaker) - this example demonstrates on how to monitor a model when the model is deployed in AWS Sagemaker with logs enabled and predict data source is **Sagemaker logs**. The reference model is a Classification model for Chest X-Ray application which takes X-Ray images input data.
- [metrics](metrics) - this folder contains the following.
-- an example for a custom Performance Monitor exporting business metrics that are not directly supported by DKube.
-- an example for a custom deployment exporting health metrics
-- an utility to query prometheus and calculate min/max/mean/std-deviation values for a metric. These are useful for deriving soft & hard thresholds
- [custom_dashboards](custom_dashboards) - this contains examples for importing custom dashboards and render them in iframes on dkube
- [precomputed_scores](precomputed_scores) - this contains example for user computing metrics and making them available via S3 object or DB table. DKube reads the metrics periodically and stores them in Prometheus. This option is available on Performance monitoring configuration screen.
