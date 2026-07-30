class DODAError(Exception):
    pass


class InvalidOperatorError(DODAError):
    pass


class InvalidProviderError(DODAError):
    pass


class InvalidFusionError(DODAError):
    pass


class InvalidStabilityMetricError(DODAError):
    pass