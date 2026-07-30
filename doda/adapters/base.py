from abc import ABC, abstractmethod


class BaseOperatorAdapter(ABC):

    """
    Converts any feature selector into
    a common DODA interface.
    """


    @abstractmethod
    def fit(self, X, y):
        pass


    @abstractmethod
    def get_importance(self):
        """
        Returns

        {
            feature: importance
        }
        """
        pass


    def get_name(self):

        return self.__class__.__name__