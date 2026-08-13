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


        # -----------------------------
        # SelectKBest / ANOVA
        # -----------------------------

        if hasattr(self.estimator, "scores_"):

            values = np.nan_to_num(
                self.estimator.scores_
            )

            print(
                "Number of scores:",
                len(values)
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

            print(
                "Number of feature importances:",
                len(values)
            )


        # -----------------------------
        # Linear models / LASSO
        # -----------------------------

        elif hasattr(self.estimator, "coef_"):

            values = np.abs(
                self.estimator.coef_
            )

            # Binary classification
            if values.ndim > 1:
                values = values[0]

            values = np.nan_to_num(
                values
            )

            print(
                "Number of coefficients:",
                len(values)
            )


        # -----------------------------
        # RFE / RFECV
        # -----------------------------

        elif hasattr(self.estimator, "ranking_"):

            ranking = np.array(
                self.estimator.ranking_,
                dtype=float
            )

            values = 1.0 / ranking

            print(
                "Number of rankings:",
                len(values)
            )


        # -----------------------------
        # VarianceThreshold
        # -----------------------------

        elif hasattr(self.estimator, "variances_"):

            values = np.nan_to_num(
                self.estimator.variances_
            )

            print(
                "Number of variances:",
                len(values)
            )


        # -----------------------------
        # Unsupported estimator
        # -----------------------------

        else:

            raise ValueError(

                f"{self.estimator.__class__.__name__} "

                "does not expose a supported "

                "feature importance attribute."

            )


        # -----------------------------
        # Convert to float
        # -----------------------------

        values = np.asarray(
            values,
            dtype=float
        )


        # -----------------------------
        # Validate dimensions
        # -----------------------------

        if len(values) != len(feature_names):

            raise ValueError(

                "Number of feature importance values "

                f"({len(values)}) does not match "

                f"number of features ({len(feature_names)})."

            )


        # -----------------------------
        # Store importance
        # -----------------------------

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