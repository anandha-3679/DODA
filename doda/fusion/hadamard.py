from .base import BaseFusion



class HadamardFusion(BaseFusion):


    def fuse(
        self,
        math_scores,
        clinical_weights
    ):


        final_scores = {}


        for feature, score in math_scores.items():


            weight = clinical_weights.get(
                feature,
                1.0
            )


            final_scores[feature] = (
                score * weight
            )


        return final_scores