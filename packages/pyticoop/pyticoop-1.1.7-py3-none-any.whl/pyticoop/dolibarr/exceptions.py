class DolibarrRequestError(Exception):
    """Exception raised for errors in Dolibarr API requests."""

    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
