import json
import asyncio
from time import sleep
from bin.connect import ApitServer


class Apit212(ApitServer):

    def __init__(self, host = "localhost", port = 8080):
        super().__init__(host, port)


class CFDRequest:

    def __init__(self, mode: str = "demo") -> None:
        """"""
        self._mode = mode

    def get_summary(self) -> json:
        """Get account summary"""
        request = {"command":"get_summary", "data":"[]", "mode": self._mode}
        return request

    def get_account(self) -> json:
        """Get account """
        request = {"command":"get_account", "data": None, "mode": self._mode}
        return request
    
