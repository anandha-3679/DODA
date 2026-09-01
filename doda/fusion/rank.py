from .base import BaseFusion


class RankFusion(BaseFusion):

    """
    Reciprocal Rank Fusion (RRF).

    Combines mathematical feature ranking with
    clinical knowledge ranking.

    RRF score:

        RRF(f) =
            1 / (k + math_rank(f))
            +
            1 / (k + clinical_rank(f))

    Higher RRF score indicates a higher final rank.
    """

    def __init__(self, k=60):

        self.k = k


    def _get_ranks(self, scores):

        """
        Convert feature scores into ranks.

        Higher score = better rank.

        Ties receive the same rank using dense ranking.
        """

        sorted_features = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        ranks = {}

        current_rank = 0
        previous_score = None

        for feature, score in sorted_features:

            if score != previous_score:

                current_rank += 1

                previous_score = score

            ranks[feature] = current_rank

        return ranks


    def fuse(
        self,
        math_scores,
        clinical_weights
    ):

        # ---------------------------------------------------------
        # Mathematical ranking
        # ---------------------------------------------------------

        math_ranks = self._get_ranks(
            math_scores
        )


        # ---------------------------------------------------------
        # Clinical ranking
        # ---------------------------------------------------------

        clinical_ranks = self._get_ranks(
            clinical_weights
        )


        # ---------------------------------------------------------
        # Reciprocal Rank Fusion
        # ---------------------------------------------------------

        final_scores = {}

        for feature in math_scores:

            math_rank = math_ranks[feature]

            clinical_rank = clinical_ranks.get(
                feature,
                len(clinical_weights) + 1
            )


            rrf_score = (

                1 / (self.k + math_rank)

                +

                1 / (self.k + clinical_rank)

            )


            final_scores[feature] = rrf_score


        return final_scores