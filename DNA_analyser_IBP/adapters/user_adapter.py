# user_connector.py


import jwt
import json
from requests import put, post, Response

from DNA_analyser_IBP.utils import Logger
from DNA_analyser_IBP.config import Config
from DNA_analyser_IBP.utils import join_url
from DNA_analyser_IBP.models import User
from DNA_analyser_IBP.utils import exception_handler
from DNA_analyser_IBP.adapters.validations import validate_text_response


class UserAdapter:
    """
    User connector providing information for current user
    """

    @staticmethod
    @exception_handler
    def sign_in(user: User) -> User:
        """
        Sign in to API http://bioinformatics.ibp.cz:8888/api

        Returns:
            tuple: JWT string, user id, expiration date
        """
        header = {
            "Accept": "text/plain",
            "Content-type": "application/json",
        }
        data: str = json.dumps({"login": user.email, "password": user.password})

        if user.email != "host":
            response: Response = put(
                join_url(user.server, Config.ENDPOINT_CONFIG.JWT),
                data=data,
                headers=header,
            )
        else:
            response: Response = post(
                join_url(user.server, Config.ENDPOINT_CONFIG.JWT), headers=header
            )

        jwt_token: str = validate_text_response(response=response, status_code=201)
        data: dict = jwt.decode(jwt_token, verify=False)
        user.set_login(jwt=jwt_token, id=data.get("id"))
        Logger.info(f"User {user.email} is successfully loged in ...")
        return user
