from abc import ABC, abstractmethod


class BaseKnowledgeProvider(ABC):


    @abstractmethod
    def get_weights(self, feature_names):

        pass