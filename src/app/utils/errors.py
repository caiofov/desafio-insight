from fastapi import HTTPException


class ItemNotFound(HTTPException):
    def __init__(self, item: str) -> None:
        super().__init__(404, item)
