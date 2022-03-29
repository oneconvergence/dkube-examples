This repository contains examples for various functions for DKube. Dkube supports Tensorflow, Pytorch, Sklearn frameworks for end to end development and deployments. To see examples for a particular framework/Language, choose the appropriate git branch.


### Branches

- tensorflow - contains examples using tensorflow + python
- pytorch - contains examples using pytorch + python
- sklearn - contains examples using sklearn + python
- R - contains examples using tensorflow + R
- monitoring - contains examples using various data sources and showcase the model monitoring feature of DKube.

### Model Monitoring Examples

- [insurance_datasources](insurance_datasources) - this example demonstrates on how to monitor a imported/deployed regression model in Dkube, where the predict data source can be **local, SQL or AWS S3**.
- [insurance_cloudevents](insurance_cloudevents) - this example demonstrates on how to monitor a model when the model is deployed with in DKube with logs enabled and predict data source is **cloudevent logs**.
- [insurance_sagemaker](insurance_sagemaker) - this example demonstrates on how to monitor a model when the model is deployed in AWS Sagemaker with logs enabled and predict data source is **Sagemaker logs**.
- [titanic](titanic) - this example demonstrates on how to monitor a imported/deployed classification model in Dkube, where the predict data source can be **local, SQL or AWS S3**.
- [metrics](metrics) - this contains an example for a custom Performance Monitor exporting business metrics that are not directly supported by DKube.
