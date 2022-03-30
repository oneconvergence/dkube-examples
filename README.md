This branch contains examples for monitoring a deployment. A deployment could be an inference service deployed on local DKube or external SageMaker/DKube clusters. The examples showcase Deployment service monitoring (Health of a deployment) as well as model drift and performance monitoring. For model monitoring, we support classification and regression models for tabular or image data. 

### Model Monitoring Examples

- [insurance_datasources](insurance_datasources) - this example demonstrates on how to monitor a imported/deployed regression model in Dkube, where the predict data source can be **local, SQL or AWS S3**.
- [insurance_cloudevents](insurance_cloudevents) - this example demonstrates on how to monitor a model when the model is deployed with in DKube with logs enabled and predict data source is **cloudevent logs**.
- [insurance_sagemaker](insurance_sagemaker) - this example demonstrates on how to monitor a model when the model is deployed in AWS Sagemaker with logs enabled and predict data source is **Sagemaker logs**.
- [titanic](titanic) - this example demonstrates on how to monitor a imported/deployed classification model in Dkube, where the predict data source can be **local, SQL or AWS S3**.
- [metrics](metrics) - this contains an example for a custom Performance Monitor exporting business metrics that are not directly supported by DKube.
