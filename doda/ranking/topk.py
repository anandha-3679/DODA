class TopKRanker:


    """
    Selects the top-k features based on
    final DODA scores.
    """


    def __init__(
        self,
        k=10
    ):

        self.k = k



    def select(
        self,
        scores
    ):

        """
        Parameters
        ----------
        scores : dict

            {
                feature_name: score
            }


        Returns
        -------
        list

            Selected feature names
        """


        if not scores:

            return []



        ranked_features = sorted(

            scores.items(),

            key=lambda x: x[1],

            reverse=True

        )


        selected = [

            feature

            for feature, score

            in ranked_features[:self.k]

        ]


        return selected