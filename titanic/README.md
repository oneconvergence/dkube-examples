# titanic

This example describe workflow of how to use projects leaderboard and featuresets.

# workflow

1. Project owner

    a. creates a project.

    b. uploads train & test datasets. 

    c. add code repo containing evaluation code. 

2. Data scientiest

    a. selects the project and launches IDE

    b. Create code, featureset, and model repos

    c. Develop preprocessing , training and predict code.

    d. Runs a pipeline which goes through all the above steps and makes a submission to the project.


# Notebooks
[owner project setup notebook](owner/resources.ipynb) - shows how to setup projects using DKube SDK.

[DS pipeline notebook](pipeline.ipynb) - Runs this notebook after launching IDE under the project. show hows to create user's DKube resources inside project using SDK and how to run end to end pipeline.



