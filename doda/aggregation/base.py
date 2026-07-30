from abc import ABC, abstractmethod


class BaseAggregator(ABC):

    """
    Interface for combining outputs
    from multiple feature selection operators.
    """


    @abstractmethod
    def aggregate(self, operator_scores):
        """
        Input:

        {
            "OperatorA":
            {
                "age":0.8,
                "bp":0.5
            },

            "OperatorB":
            {
                "age":0.7,
                "bp":0.9
            }
        }


        Output:

        {
            "age":0.75,
            "bp":0.7
        }

        """

        pass