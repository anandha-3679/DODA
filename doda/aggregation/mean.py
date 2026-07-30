from .base import BaseAggregator


class MeanAggregator(BaseAggregator):

    """
    Simple average aggregation.
    """


    def aggregate(self, operator_scores):

        combined = {}


        for operator, scores in operator_scores.items():

            for feature, value in scores.items():

                if feature not in combined:
                    combined[feature] = []


                combined[feature].append(value)



        final_scores = {}


        for feature, values in combined.items():

            final_scores[feature] = (
                sum(values) / len(values)
            )


        return final_scores