from abc import ABC, abstractmethod


class BaseKnowledgeProvider(ABC):
    """
    Interface for external domain knowledge sources.
    """

    @abstractmethod
    def get_weights(self, feature_names):
        """
        Return domain weights.

        Example:

        {
            "age": 0.9,
            "blood_pressure": 0.8
        }

        """
        pass