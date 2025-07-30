"""
"""

import json

from pydantic import BaseModel
import requests

class UserConfig(BaseModel):

    url: str
    email: str
    password: str
    authorization: str | None = None

    def get_jwt(self) -> None:
        """
        Retrieves JWT for the user specified in `self.admin_config`

        Raises
        ------
        jwt_exc
            general failure exception
        """

        try:
            s = requests.Session()
            header = {"Content-Type": "application/json"}
            payload = json.dumps(
                {
                    "email": self.email,
                    "password": self.password,
                }
            )
            url = self.url + "/login"
            with s.post(url, data=payload, headers=header) as response:
                user_data = response.json()

            print(f"Retrieved JWT for user {self.email}")
            self.authorization = "Bearer " + user_data["token"]
        except Exception as jwt_exc:
            print(f"Failed to retrieve JWT for user {self.email}")
            raise jwt_exc
