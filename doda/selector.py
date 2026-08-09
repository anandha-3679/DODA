from sklearn.base import BaseEstimator, TransformerMixin

from .pipeline import DODAPipeline
from .ranking import TopKRanker
import pandas as pd


class DODASelector(
    BaseEstimator,
    TransformerMixin
):

    """
    Public DODA interface.

    Users interact only with this class.
    """


    def __init__(
        self,
        operators=None,
        aggregator=None,
        provider=None,
        fusion=None,
        stability_metrics=None,
        top_k=10,
        ranker=None
    ):

        self.operators = operators or []

        self.aggregator = aggregator

        self.provider = provider

        self.fusion = fusion

        self.stability_metrics = stability_metrics or []

        self.top_k = top_k

        # allow custom ranking strategies
        self.ranker = ranker



    def fit(self, X, y):


        self.pipeline = DODAPipeline(

            operators=self.operators,

            aggregator=self.aggregator,

            provider=self.provider,

            fusion=self.fusion,

            stability_metrics=self.stability_metrics,

            top_k=self.top_k
        )


        results = self.pipeline.execute(
            X,
            y
        )


        # Store final scores

        self.raw_math_scores_ = (
            results["raw_math_scores"]
        )

        self.math_scores_ = (
            results["math_scores"]
        )


        self.clinical_weights_ = (
            results["clinical_weights"]
        )


        self.final_scores_ = (
            results["final_scores"]
        )

        # -----------------------------
        # Ranking Layer
        # -----------------------------

        if self.ranker is None:

            self.ranker = TopKRanker(
                self.top_k
            )


        self.selected_features_ = (
            self.ranker.select(
                self.final_scores_
            )
        )


        print(
            "Top",
            self.top_k,
            "Features Selected:",
            self.selected_features_
        )



        self.stability_report_ = {}


        return self



    def transform(self, X):


        if not hasattr(
            self,
            "selected_features_"
        ):

            raise RuntimeError(
                "DODASelector must be fitted first"
            )



        if len(self.selected_features_) == 0:

            return X



        return X[
            self.selected_features_
        ]



    def fit_transform(
        self,
        X,
        y
    ):

        self.fit(
            X,
            y
        )

        return self.transform(
            X
        )



    def get_math_scores(self):

        return self.math_scores_

    def get_clinical_weights(self):

        return self.clinical_weights_


    def get_final_scores(self):

        return self.final_scores_


    def get_selected_features(self):

        return self.selected_features_


    def compare_scores(self):

        """
        Compare mathematical ranking vs
        clinically fused DODA ranking.
        """

        import pandas as pd


        features = list(
            self.final_scores_.keys()
        )


        # Mathematical ranking

        math_ranked = sorted(
            self.math_scores_.items(),
            key=lambda x: x[1],
            reverse=True
        )


        math_rank = {

            feature: idx + 1

            for idx, (feature, score)
            in enumerate(math_ranked)

        }


        # Final DODA ranking

        final_ranked = sorted(
            self.final_scores_.items(),
            key=lambda x: x[1],
            reverse=True
        )


        final_rank = {

            feature: idx + 1

            for idx, (feature, score)
            in enumerate(final_ranked)

        }



        rows = []


        for feature in features:


            rows.append({

                "Feature":

                feature,


                "Math Rank":

                math_rank[feature],


                "Normalized Math Score":

                round(
                    self.math_scores_.get(
                        feature,
                        0
                    ),
                    4
                ),


                "Clinical Weight":

                round(
                    self.clinical_weights_.get(
                        feature,
                        1.0
                    ),
                    4
                ),


                "DODA Rank":

                final_rank[feature],


                "Final Score":

                round(
                    self.final_scores_.get(
                        feature,
                        0
                    ),
                    4
                ),


                "Rank Change":

                math_rank[feature]
                -
                final_rank[feature]

            })


        df = pd.DataFrame(rows)


        return (

            df

            .sort_values(
                by="DODA Rank"
            )

            .reset_index(
                drop=True
            )

        )

                