def validate_input(X,y):


    if len(X) != len(y):

        raise ValueError(
            "X and y have different number of rows"
        )



    if X.empty:

        raise ValueError(
            "Input dataset is empty"
        )



    if X.columns.duplicated().any():

        raise ValueError(
            "Duplicate feature names detected"
        )



    return True