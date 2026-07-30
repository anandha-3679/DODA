from .utils.validation import validate_input
from .utils.preprocessing import preprocess_data

from .knowledge.engine import KnowledgeEngine
from .fusion.hadamard import HadamardFusion


class DODAPipeline:

    def __init__(
        self,
        operators=None,
        aggregator=None,
        provider=None,
        fusion=None,
        stability_metrics=None,
        top_k=10
    ):

        self.operators = operators or []

        self.aggregator = aggregator

        self.provider = provider

        self.knowledge_engine = KnowledgeEngine(
            provider
        )

        self.fusion = fusion or HadamardFusion()

        self.stability_metrics = stability_metrics or []

        self.top_k = top_k

        self.selection_history = []



    def execute(self, X, y):

        validate_input(X, y)

        X = preprocess_data(X)

        print("DODA Pipeline Started")


        # ---------------------------------
        # Step 1 : Mathematical Operators
        # ---------------------------------

        operator_scores = self.run_operators(
            X,
            y
        )

        print("Operator Scores:")
        print(operator_scores)


        # ---------------------------------
        # Step 2 : Aggregate Math Scores
        # ---------------------------------

        math_scores = self.resolve_scores(
            operator_scores
        )

        print("\nMathematical Scores")
        print(math_scores)


        # ---------------------------------
        # Step 3 : Clinical Knowledge Layer
        # ---------------------------------

        if self.provider is not None:

            clinical_weights = self.knowledge_engine.get_weights(
                list(math_scores.keys())
            )

        else:

            clinical_weights = {

                feature: 1.0

                for feature in math_scores

            }

        print("\nClinical Weights")
        print(clinical_weights)


        # ---------------------------------
        # Step 4 : Fusion Layer
        # ---------------------------------
                
        if self.fusion is not None:

            final_scores = self.fusion.fuse(

                math_scores,

                clinical_weights

            )

        else:

            final_scores = math_scores


        print("\nFinal DODA Scores")
        print(final_scores)


        # ---------------------------------
        # Save Selection History
        # ---------------------------------

        self.selection_history.append(

            list(final_scores.keys())

        )


        # ---------------------------------
        # Return Results
        # ---------------------------------

        return {

            "math_scores": math_scores,

            "clinical_weights": clinical_weights,

            "final_scores": final_scores

        }



    def run_operators(self, X, y):

        results = {}

        for operator in self.operators:

            print(

                "Running:",

                operator.get_name()

            )

            operator.fit(

                X,

                y

            )

            operator_name = (

                operator.get_name()

                + "_"

                + str(len(results) + 1)

            )

            results[

                operator_name

            ] = operator.get_importance()

        return results



    def resolve_scores(self, operator_scores):

        number_of_operators = len(

            operator_scores

        )

        print(

            "Resolving scores from:",

            number_of_operators,

            "operators"

        )


        # No operators

        if number_of_operators == 0:

            return {}


        # Single operator

        if number_of_operators == 1:

            return list(

                operator_scores.values()

            )[0]


        # Multiple operators

        if self.aggregator is None:

            raise ValueError(

                "Multiple operators detected. "

                "Please provide an aggregator."

            )


        return self.aggregator.aggregate(

            operator_scores

        )