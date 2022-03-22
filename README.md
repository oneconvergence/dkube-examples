This repository contains examples for various functions for DKube. Dkube supports Tensorflow, Pytorch, Sklearn frameworks for end to end development and deployments. To see examples for a particular framework/Language, choose the appropriate git branch.


### Branches

- tensorflow - contains examples using tensorflow + python
- pytorch - contains examples using pytorch + python
- sklearn - contains examples using sklearn + python
- R - contains examples using tensorflow + R
- monitoring - contains examples using various frameworks and showcase the model monitoring feature of DKube.

### Examples

- [insurance](insurance) - this example demonstrates on how to monitor the regression model in Dkube.
- [titanic](titanic) - this example demonstrates on how to monitor the classification model in Dkube.
- [insurance_cloudevents](insurance_cloudevents) - this example demonstrates on how to monitor the regression model when the predict data source is cloudevents.
- [insurance_sagemaker](insurance_sagemaker) - this example demonstrates the deployment of model into sagemaker (outside Dkube) and monitoring on Dkube.
- [metrics](metrics) - this contains an example for a custom Performance Monitor exporting business metrics that are not directly supported by DKube.
