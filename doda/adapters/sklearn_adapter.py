import numpy as np

from .base import BaseOperatorAdapter


class SklearnAdapter(BaseOperatorAdapter):


    def __init__(self, estimator):

        self.estimator = estimator

        self.importance = {}


    def fit(self, X, y):

        self.estimator.fit(X, y)

        self._extract_importance(X)

        return self


    def _extract_importance(self, X):

        feature_names = list(X.columns)

        print("DODA feature order:")
        print(feature_names[:10])

        print("Number of features:", len(feature_names))

        print("Number of scores:", len(self.estimator.scores_))


        # -----------------------------
        # SelectKBest
        # -----------------------------

        if hasattr(self.estimator, "scores_"):

            values = np.nan_to_num(
                self.estimator.scores_
            )


        # -----------------------------
        # Tree models
        # -----------------------------

        elif hasattr(
            self.estimator,
            "feature_importances_"
        ):

            values = np.nan_to_num(
                self.estimator.feature_importances_
            )


        # -----------------------------
        # Linear models
        # -----------------------------

        elif hasattr(self.estimator, "coef_"):

            scores = np.abs(
                self.estimator.coef_
            )

            # Binary classification
            if scores.ndim > 1:
                scores = scores[0]


        # -----------------------------
        # RFE / RFECV
        # -----------------------------

        elif hasattr(self.estimator, "ranking_"):

            ranking = np.array(
                self.estimator.ranking_,
                dtype=float
            )

            values = 1.0 / ranking


        # -----------------------------
        # VarianceThreshold
        # -----------------------------

        elif hasattr(self.estimator, "variances_"):

            values = np.nan_to_num(
                self.estimator.variances_
            )


        else:

            raise ValueError(

                f"{self.estimator.__class__.__name__} "

                "does not expose a supported "

                "feature importance attribute."

            )


        values = values.astype(float)


        self.importance = dict(

            zip(

                feature_names,

                values

            )

        )


    def get_importance(self):

        return self.importance


    def get_name(self):

        return self.estimator.__class__.__name__