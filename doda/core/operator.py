from abc import ABC, abstractmethod


class BaseOperator(ABC):

    """
    Every DODA operator must follow this contract.
    """


    @abstractmethod
    def fit(self, X, y):
        """
        Train operator on data.
        """
        pass



    @abstractmethod
    def get_scores(self):
        """
        Return feature scores.

        Example:

        {
            "age":0.8,
            "bp":0.5
        }

        """
        pass



    def get_name(self):

        return self.__class__.__name__