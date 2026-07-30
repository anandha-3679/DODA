from abc import ABC, abstractmethod


class BaseFusion(ABC):


    @abstractmethod
    def fuse(
        self,
        math_scores,
        clinical_weights
    ):

        pass