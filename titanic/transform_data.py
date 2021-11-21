class Transformer():
    def preprocess(self,dataframe):
        import pandas as pd
        data_to_preprocess = dataframe 
        data_to_preprocess["Age"].fillna(value=data_to_preprocess["Age"].median(), inplace=True)
        features = ["Pclass", "Sex", "SibSp", "Parch"]
        train_df = pd.get_dummies(data_to_preprocess[features])
        data_to_preprocess = pd.concat([data_to_preprocess[["Age", "Fare", "Survived", "PassengerId","timestamp"]], train_df], axis=1)
        preprocessed_data = data_to_preprocess
        return preprocessed_data
