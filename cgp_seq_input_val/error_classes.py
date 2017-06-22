"""Package error classes"""

class SeqValidationError(RuntimeError):
    """Exception for failures to validate data in the manifest."""
    pass

class ConfigError(RuntimeError):
    """
    Exception for errors in the values of config/*.json files.
    """
    pass

class ParsingError(RuntimeError):
    """
    Exception for errors in the naming of the config/*.json files.
    """
    pass

class ValidationError(RuntimeError):
    """
    Exception for failures to validate data in the manifest.
    """
    pass
