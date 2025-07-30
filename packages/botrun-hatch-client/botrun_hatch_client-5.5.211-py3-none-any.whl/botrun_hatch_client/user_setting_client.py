import os
from typing import Union
import aiohttp
from dotenv import load_dotenv

from botrun_hatch.models.user_setting import UserSetting

load_dotenv()


class UserSettingClient:
    def __init__(self):
        self.base_url = os.getenv(
            "BOTRUN_FLOW_LANG_URL",
            "https://botrun-flow-lang-fastapi-dev-36186877499.asia-east1.run.app",
        )
        self.api_url = f"{self.base_url}/api/user_setting"

    async def create_user_setting(
        self, user_setting: UserSetting
    ) -> Union[UserSetting, None]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url, json=user_setting.model_dump()
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return UserSetting(**data)
                else:
                    print(f"Error creating user setting: Status code {response.status}")
                    return None

    async def get_user_setting(self, user_id: str) -> Union[UserSetting, None]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/{user_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    return UserSetting(**data)
                elif response.status == 404:
                    print(f"No user setting found for user {user_id}")
                    return None
                else:
                    print(
                        f"Error getting user setting for user {user_id}: Status code {response.status}"
                    )
                    return None

    async def update_user_setting(
        self, user_id: str, user_setting: UserSetting
    ) -> Union[UserSetting, None]:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.api_url}/{user_id}", json=user_setting.model_dump()
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return UserSetting(**data)
                else:
                    print(
                        f"Error updating user setting for user {user_id}: Status code {response.status}"
                    )
                    return None
