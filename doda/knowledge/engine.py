class KnowledgeEngine:


    def __init__(self, provider):

        self.provider = provider

        print(
            "Provider inside knowledge engine:",
            self.provider
        )



    def get_weights(self, features):

        # No provider supplied
        # Neutral clinical weight

        if self.provider is None:

            return {

                feature: 1.0

                for feature in features

            }


        # Delegate to provider

        return self.provider.get_weights(
            features
        )