from abc import ABC, abstractmethod


class BaseFusion(ABC):
    """
    Interface for combining mathematical
    scores with domain knowledge.
    """

    @abstractmethod
    def combine(
        self,
        math_scores,
        knowledge_weights
    ):
        pass