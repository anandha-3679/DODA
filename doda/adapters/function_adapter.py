from .base import BaseOperatorAdapter


class FunctionAdapter(BaseOperatorAdapter):


    def __init__(self, function):

        self.function = function

        self.importance = {}


    def fit(self, X, y):

        self.importance = self.function(
            X,
            y
        )

        return self


    def get_importance(self):

        return self.importance


    def get_name(self):

        return self.function.__name__