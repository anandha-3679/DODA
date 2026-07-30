import pandas as pd



def preprocess_data(X):


    if not isinstance(
        X,
        pd.DataFrame
    ):

        X = pd.DataFrame(X)



    return X