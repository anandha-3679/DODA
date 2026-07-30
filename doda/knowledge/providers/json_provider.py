import json

from .base import BaseKnowledgeProvider


class JSONProvider(BaseKnowledgeProvider):


    def __init__(self, path):

        self.path = path

        with open(path, "r") as f:
            self.weights = json.load(f)



    def get_weights(self, feature_names):

        result = {}

        for feature in feature_names:

            result[feature] = self.weights.get(
                feature,
                1.0
            )

        return result
    