"""
Executes workflow:

- Create new file category
- Upload new file
- Process file
- Create new application
"""

import json
from collections.abc import Generator
from pathlib import Path

import requests
from pydantic import BaseModel


class FileCategoryCreationResponse(BaseModel):


    id: int
    categoryName: str
    isActive: bool
    accountId: int
    chunkSize: int | None
    chunkOverlap: int | None
    createdAt: str | None
    updatedAt: str | None
    Region: list


class FileUploadResponse(BaseModel):

    id: int
    accountId: int
    moduleId: int | None
    productCategoryId: int
    size: int
    docName: str
    blobUrl: str
    docType: str | None
    location: str | None
    tags: str
    status: str
    uploadedBy: int
    createdAt: str | None
    updatedAt: str | None
    applicationId: int | None


class FileProcessingProgressResponse(BaseModel):

    id: int
    status: str
    per: int


class FileProcessingFinishResponse(BaseModel):

    id: int
    accountId: int
    moduleId: int | None
    productCategoryId: int
    size: int
    docName: str
    blobUrl: str
    docType: str | None
    location: str | None
    tags: str
    status: str
    uploadedBy: int
    createdAt: str | None
    updatedAt: str | None
    applicationId: int | None


class ApplicationCreationResponse(BaseModel):

    id: int
    accountId: int
    moduleId: int
    name: str
    description: str | None
    theme: str
    type: str | None
    hint: str | None
    isActive: bool
    showQuestionSuggestion: bool
    templateId: int | None
    createdAt: str | None
    updatedAt: str | None
    Suggestion: list


class AdminConfig(BaseModel):

    url: str
    email: str
    password: str
    authorization: str | None = None


class AdminWorkflow(BaseModel):

    admin_config: AdminConfig
    file_category_id: int | None = None
    file_ids: list[int] = []
    file_statuses: dict[int, str] = {}
    application_id: int | None = None

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
                    "email": self.admin_config.email,
                    "password": self.admin_config.password,
                }
            )
            url = self.admin_config.url + "/login"
            with s.post(url, data=payload, headers=header) as response:
                user_data = response.json()

            print(f"Retrieved JWT for user {self.admin_config.email}")
            self.admin_config.authorization = "Bearer " + user_data["token"]
        except Exception as jwt_exc:
            print(f"Failed to retrieve JWT for user {self.admin_config.email}")
            raise jwt_exc

    def create_file_category(self, name: str) -> FileCategoryCreationResponse:
        """
        Creates a new file category with specified name

        Parameters
        ----------
        name : str
            name of the new file category

        Returns
        -------
        FileCategoryCreationResponse
            JSON response received upon successful file category creation

        Raises
        ------
        file_cat_exc
            general failure exception
        """

        try:
            s = requests.Session()
            headers = {
                "Content-Type": "application/json",
                "Authorization": self.admin_config.authorization,
            }
            url = self.admin_config.url + "/admin/category"
            payload = json.dumps({"categoryName": name, "regions": []})

            with s.post(url, data=payload, headers=headers) as response:
                category_data = FileCategoryCreationResponse(**response.json())

            self.file_category_id = category_data.id
            return category_data
        except Exception as file_cat_exc:
            print(f"Failed to create file category: {name}")
            raise file_cat_exc

    def upload_files(
        self, filepaths: list[str]
    ) -> Generator[FileUploadResponse]:
        """
        Upload files to the currently specified file category

        Parameters
        ----------
        filepaths : list[str]
            list of paths to files

        Yields
        ------
        FileUploadResponse
            JSON response received upon successful file upload

        Raises
        ------
        exc
            FileUploadResponse validation failure
        """
        s = requests.Session()
        headers = {"Authorization": self.admin_config.authorization}
        url = self.admin_config.url + "/admin/upload/file"
        payload = {
            "tags": "kds_april",
            "productCategoryId": self.file_category_id,
        }

        for filepath in filepaths:
            with s.post(
                url,
                files={
                    "file": (
                        Path(filepath).name,
                        open(Path(filepath), "rb"),
                        "application/pdf",
                    )
                },
                data=payload,
                headers=headers,
            ) as response:
                try:
                    upload_data = FileUploadResponse(**response.json())
                except Exception as exc:
                    print("Upload process received an unexpected response")
                    raise exc

            self.file_ids.append(upload_data.id)
            self.file_statuses[upload_data.id] = "INIT"
            yield upload_data

    def process_files(
        self,
    ) -> Generator[
        FileProcessingProgressResponse | FileProcessingFinishResponse
    ]:
        """
        Trigger processing of all recently uploaded files

        Yields
        ------
        FileProcessingProgressResponse | FileProcessingFinishResponse
            JSON status response received during file processing

        Raises
        ------
        file_exc
            general failure exception
        """
        try:
            s = requests.Session()

            for file_id in self.file_ids:
                url = self.admin_config.url + f"/admin/file/process/{file_id}"
                with s.get(url, stream=True) as response:
                    curr_status = ""

                    for line in response.iter_lines():
                        if line:
                            # line looks like this:
                            # b'data: {"id":200,"status":"EXTRACTING","per":50}'
                            curr_res = json.loads(
                                line.decode().split("data: ")[1]
                            )
                            if not curr_res["status"] == curr_status:
                                # every time the status changes, we want to update
                                # the class attribute and yield the new status
                                curr_status = curr_res["status"]
                                self.file_statuses[file_id] = curr_status
                                if not curr_status == "DONE":
                                    yield FileProcessingProgressResponse(
                                        **curr_res
                                    )
                yield FileProcessingFinishResponse(**curr_res)
        except Exception as file_exc:
            print(f"Failed to process file id={file_id}")
            raise file_exc

    def create_application(self, name: str) -> ApplicationCreationResponse:
        """
        Create a new application from the attached file category

        Parameters
        ----------
        name : str
            name of the application

        Returns
        -------
        ApplicationCreationResponse
            JSON response received upon successful application creation

        Raises
        ------
        app_exc
            general failure exception
        """

        try:
            s = requests.Session()
            headers = {
                "Content-Type": "application/json",
                "Authorization": self.admin_config.authorization,
            }
            url = self.admin_config.url + "/admin/application"
            payload = json.dumps(
                {
                    "name": name,
                    "productCategory": [self.file_category_id],
                    "regions": [],
                    "moduleId": 2,  # hardcoded moduleId for Infinite FAQ
                    "suggestions": [],
                }
            )
            with s.post(url, data=payload, headers=headers) as response:
                app_data = ApplicationCreationResponse(**response.json())

            self.application_id = app_data.id
            return app_data
        except Exception as app_exc:
            print(f"Failed to create new application: {name}")
            raise app_exc
