class ExtractionFailedException(ValueError):
    """
    Exception raised when a field could not be found
    in the input file.
    """

    FAILED_EXTRACTION_MSG = "Could not extract '%s' from HTML. Has the HTML structure changed?"

    def __init__(self, field):
        self.field = field
        self.msg= self.FAILED_EXTRACTION_MSG % field

    def __repr__(self):
        return 'field=self.field'

    def __str__(self):
        return self.msg
