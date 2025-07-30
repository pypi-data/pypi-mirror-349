import os
from typing import Union, BinaryIO
import aiohttp
import json
from dotenv import load_dotenv
from io import BytesIO


load_dotenv()


class StorageClient:
    def __init__(self):
        self.base_url = os.getenv(
            "BOTRUN_FLOW_LANG_URL",
            "https://botrun-flow-lang-fastapi-dev-36186877499.asia-east1.run.app",
        )
        self.api_url = f"{self.base_url}/api/files"

    async def upload_file(
        self, user_id: str, file_path: str, file_info: dict
    ) -> tuple[bool, str]:
        """
        Upload a file to storage
        """
        try:
            async with aiohttp.ClientSession() as session:
                with open(file_path, "rb") as f:
                    file_data = aiohttp.FormData()
                    file_data.add_field("file", f)
                    file_data.add_field("file_info", json.dumps(file_info))

                    async with session.post(
                        f"{self.api_url}/{user_id}", data=file_data
                    ) as response:
                        if response.status == 200:
                            return True, "File uploaded successfully"
                        else:
                            error_msg = (
                                f"Error uploading file: Status code {response.status}"
                            )
                            print(error_msg)
                            return False, error_msg
        except Exception as e:
            error_msg = f"Error uploading file: {str(e)}"
            print(error_msg)
            return False, error_msg

    async def get_file(self, user_id: str, file_id: str) -> Union[BytesIO, None]:
        """
        Get a file from storage
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/{user_id}/{file_id}"
                ) as response:
                    if response.status == 200:
                        content = await response.read()
                        return BytesIO(content)
                    else:
                        print(
                            f"Error getting file {file_id}: Status code {response.status}"
                        )
                        return None
        except Exception as e:
            print(f"Error getting file: {str(e)}")
            return None

    async def delete_file(self, user_id: str, file_id: str) -> tuple[bool, str]:
        """
        Delete a file from storage
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    f"{self.api_url}/{user_id}/{file_id}"
                ) as response:
                    if response.status == 200:
                        return True, "File deleted successfully"
                    else:
                        error_msg = f"Error deleting file {file_id}: Status code {response.status}"
                        print(error_msg)
                        return False, error_msg
        except Exception as e:
            error_msg = f"Error deleting file: {str(e)}"
            print(error_msg)
            return False, error_msg
