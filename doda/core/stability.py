from abc import ABC, abstractmethod


class BaseStabilityMetric(ABC):
    """
    Interface for stability evaluation.
    """

    @abstractmethod
    def compute(self, history):
        """
        history:

        [
            ["age", "bp"],
            ["age", "cholesterol"]
        ]

        """
        pass