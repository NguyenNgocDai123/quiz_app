from typing_extensions import TypedDict


class Code(TypedDict):
    code: int
    message: str


class BusinessCode:
    #  Auth
    LOGIN_SUCCESS: Code = Code(code=1, message="Login success")
    REGISTER_SUCCESS: Code = Code(code=2, message="Register success")
    PASSWORD_RESET_SUCCESS: Code = Code(code=3,
                                        message="Password reset success")
    PASSWORD_INVALID: Code = Code(code=4, message="Password invalid")
    REFRESH_TOKEN_NOT_FOUND: Code = Code(code=5,
                                         message="Refresh Token not found")
    #  User
    USER_NOT_FOUND: Code = Code(code=1001, message="User not found")
    USER_ALREADY_EXISTS: Code = Code(code=1002, message="User already exists")
    USER_NOT_ACTIVE: Code = Code(code=1003, message="User not active")
    USER_NOT_AUTHORIZED: Code = Code(code=1004, message="User not authorized")
    USER_PASSWORD_INCORRECT: Code = Code(code=1005,
                                         message="User password incorrect")
    USER_TOKEN_EXPIRED: Code = Code(code=1006, message="User token expired")
    USER_TOKEN_INVALID: Code = Code(code=1007, message="User token invalid")

    #  Group
    GROUP_NOT_FOUND: Code = Code(code=2001, message="Group not found")
    GROUP_ALREADY_EXISTS: Code = Code(code=2002, message="Group already exists")
    GROUP_NOT_ACTIVE: Code = Code(code=2003, message="Group not active")
    GROUP_NOT_AUTHORIZED: Code = Code(code=2004, message="Group not authorized")

    # Folder
    FOLDER_NOT_FOUND: Code = Code(code=3001, message="Folder not found")
    FOLDER_NOT_ACCESS: Code = Code(code=3002, message="Folder not accessible")
    FOLDER_MOVE_INVALID: Code = Code(code=3003, message="Folder move invalid")
    INVALID_OPERATION: Code = Code(code=3004, message="Invalid operation")
    FOLDER_DEPTH_EXCEEDED: Code = Code(code=3005,
                                       message="Folder depth exceeded")

    # Ng_Words
    NG_WORD_NOT_FOUND: Code = Code(code=4001, message="Ng_words not found")
    NG_WORD_ALREADY_EXISTS: Code = Code(code=4002,
                                        message="Ng_words already exists")
    NG_WORD_DETECTED: Code = Code(
        code=4009, message="The prompt contains prohibited words."
    )

    #   Token_setting
    TOKEN_SETTING_NOT_FOUND: Code = Code(code=4003,
                                         message="Token_setting not found")
    TOKEN_SETTING_ALREADY_EXISTS: Code = Code(
        code=4004, message="Token_setting already exists"
    )

    #   Roles
    ROLE_NOT_FOUND: Code = Code(code=4005, message="Roles not found")
    ROLE_ALREADY_EXISTS: Code = Code(code=4006, message="Roles already exists")

    #   prompt_template
    PROMPT_TEMPLATE_NOT_FOUND: Code = Code(
        code=4007, message="Prompt_template not found"
    )
    PROMPT_TEMPLATE_ALREADY_EXISTS: Code = Code(
        code=4008, message="Prompt_template already exists"
    )

    # GenModel
    GEN_MODEL_NOT_FOUND: Code = Code(code=5001, message="GenModel not found")
    GEN_MODEL_ALREADY_EXISTS: Code = Code(code=5002,
                                          message="GenModel already exists")

    # ChatBot
    CHATBOT_NOT_FOUND: Code = Code(code=6001, message="ChatBot not found")
    CHATBOT_ACCESS_DENIED: Code = Code(code=6002,
                                       message="ChatBot access denied")

    # Document
    DOCUMENT_NOT_FOUND: Code = Code(code=6100, message="Document not found")
    CONTAIN_DOCUMENT_UNVALID: Code = Code(
        code=6003, message="Contain document unvalid: {document_ids}"
    )
    DOCUMENT_ALREADY_EXISTS: Code = Code(code=6101,
                                         message="Document already exists")
    DOCUMENT_NOT_ACCESS: Code = Code(code=6102, 
                                     message="Document not accessible")
    DOCUMENT_NOT_ACTIVE: Code = Code(code=6103,
                                     message="Document not active")
    DOCUMENT_NOT_AUTHORIZED: Code = Code(code=6104, message="Document not authorized")

    # Image
    IMAGE_NOT_FOUND: Code = Code(code=6501, message="Image not found")

    #  Conversation
    CONVERSATION_NOT_FOUND: Code = Code(code=7001, message="Conversation not found")

    #  Token History
    TOKEN_HISTORY_NOT_FOUND: Code = Code(code=8001, message="Token history not found")
    DATA_NOT_FOUND: Code = Code(code=8002, message="Token history data not found")

    #  Message History
    MESSAGE_HISTORY_NOT_FOUND: Code = Code(
        code=9001, message="Message history not found"
    )

    # MetaData
    META_DATA_NOT_FOUND: Code = Code(code=10001, message="Meta Data not found")
    META_DATA_ALREADY_EXISTS: Code = Code(
        code=10002, message="Meta Data already exists"
    )
    META_DATA_SQL_INJECT_ERROR: Code = Code(
        code=10003,
        message="SQL injection error: {error_message}",
    )

    @classmethod
    def get_message(cls, code: int) -> str:
        """
        Retrieves a message based on the provided business code.

        Args:
            code (int): The business code to retrieve the message for.

        Returns:
            str: The message associated with the business code, or "Unknown Business Code" if not found.
        """
        for attr in cls.__annotations__.keys():
            if getattr(cls, attr)["code"] == code:
                return getattr(cls, attr)["message"]
        return "Unknown Business Code"
