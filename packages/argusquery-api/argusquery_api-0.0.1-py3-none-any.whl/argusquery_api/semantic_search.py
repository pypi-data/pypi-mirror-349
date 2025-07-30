"""
Module for conducting semantic search on the ArgusQuery API
"""

import json
from collections.abc import Generator
from pathlib import Path

import requests
from pydantic import BaseModel

from .auth import UserConfig


class SearchAnswerProgressResponse(BaseModel):
    """
    Models the JSON response for search. This response schema is for
    in-progress responses only

    ATTRIBUTES
    ----------
    questionId : int
    convoId : int
    text : str
    sender : str
    rating : int = 0
    source : list[dict]
    commentAdded : bool = False
    completion : bool = False
    """

    questionId: int
    convoId: int
    text: str
    sender: str
    rating: int = 0
    source: list[dict]
    commentAdded: bool = False
    completion: bool = False


class SearchAnswerFinishResponse(BaseModel):
    """
    Models the JSON response for search. This response schema is for fully
    completed responses only

    ATTRIBUTES
    ----------
    answerId : int
    questionId : int
    convoId : int
    text : str
    sender : str
    rating : int = 0
    source : list[dict]
    commentAdded : bool = False
    completion : bool = True
    """

    answerId: int
    questionId: int
    convoId: int
    text: str
    sender: str
    rating: int = 0
    source: list[dict]
    commentAdded: bool = False
    completion: bool = True


class SemanticSearch(BaseModel):

    user_config: UserConfig
    account_id: int
    application_id: int
    module_id: int | None = None

    def search(
        self, query: str, stream=True, text_only=False
    ) -> Generator[
        tuple[int, SearchAnswerProgressResponse | SearchAnswerFinishResponse]
        | str
    ]:
        """
        Executes search process given a user query. Note the return types
        specific to parameter values

        Parameters
        ----------
        query : str
            user query string
        stream : bool, optional
            emulate streaming with `requests`; by default True
        text_only : bool, optional
            ignore yielding a JSON response and simply print text instead.
            Entire output will be printed to the same line, but LLM formatting
            will make it pretty; by default False

        Yields
        ------
        Generator[
            tuple[
                int,
                SearchAnswerProgressResponse | SearchAnswerFinishResponse
            ]
            | str
        ]
            this generator is the result of `iterlines()` called on the JSON
            response; if stream is `False`, it iterates only once; if text_only
            is `True`, yields a string; all other cases yield one or more
            tuples containing the HTTP status code and the JSON response body

        Raises
        ------
        search_exc
            general failure exception
        """

        try:
            s = requests.Session()
            headers = {
                "Content-Type": "application/json",
                "Authorization": self.user_config.authorization,
            }
            url = self.user_config.url + "/conversation/search"
            payload = json.dumps(
                {
                    "applicationId": self.application_id,
                    "moduleId": self.module_id,
                    "question": query,
                }
            )
            with s.post(
                url, data=payload, headers=headers, stream=stream
            ) as response:
                curr_text = ""

                for line in response.iter_lines():
                    if line:
                        # first line looks like this:
                        # b'data: {"convoId":6295,"questionId":7072,"text":"The","sender":"bot","rating":0,"source":[{}],"commentAdded":false,"completion":false}'

                        # last line looks like this:
                        # b'data: {"answerId":6728,"questionId":7072,"convoId":6295,"text":"...","sender":"bot","rating":0,"source":[{}],"commentAdded":false,"completion":true}'
                        curr_res: dict = json.loads(
                            line.decode().split("data: ")[1]
                        )
                        if "text" in curr_res.keys():
                            if curr_text:
                                next_text = curr_res["text"].split(curr_text)[
                                    1
                                ]
                                curr_text = curr_res["text"]
                                # find the diff between the current text and
                                # the previous to emulate streaming
                            else:
                                # set next print to be the beginning of the
                                # response
                                curr_text = curr_res["text"]
                                next_text = curr_text

                            if not text_only:
                                if not curr_res["completion"]:
                                    search_data = SearchAnswerProgressResponse(
                                        **curr_res
                                    )
                                else:
                                    search_data = SearchAnswerFinishResponse(
                                        **curr_res
                                    )
                                yield (response.status_code, search_data)
                            else:
                                print(next_text, end="")

        except Exception as search_exc:
            print("Semantic search encountered an exception")
            raise search_exc
