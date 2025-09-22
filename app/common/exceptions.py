from app.constants.business_code import BusinessCode


class BusinessException(Exception):
    """
    Custom exception for business logic errors.
    """

    def __init__(self, business_code: int, message: str = None) -> None:
        """
        Args:
            business_code (dict): The business code from BusinessCode.
            status_code (int): The HTTP status code for the exception.
        """
        self.business_code = business_code
        self.message = message or BusinessCode.get_message(business_code)
