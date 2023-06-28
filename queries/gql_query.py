from abc import ABC, abstractmethod
import hashlib
import aiohttp
import json

SPOTIFY_PARTNER_URL = "https://api-partner.spotify.com"

class GQLQuery():
    name: str
    endpoint: str
    gql_query: str
    gql_query_hash: str

    __client: aiohttp.ClientSession # Reference to client in App
    __headers: dict # Reference to headers in App

    def __init__(self, client: aiohttp.ClientSession, headers: dict):
        self.gql_query_hash = hashlib.sha256(self.gql_query.encode("utf-8")).hexdigest()
        self.__client = client
        self.__headers = headers

    
    @abstractmethod
    def get_variables(self, id: str) -> dict:
        pass

    @abstractmethod
    def parse_response(self, response_json: dict) -> dict:
        return response_json

    def __get_extensions(self) -> dict:
        return {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": self.gql_query_hash
            }
        }
    
    # All queries require either an album or artist ID, so we only need ID as a parameter
    async def send_query(self, id: str) -> dict:
        params = {
            "operationName": self.name, 
            "variables": json.dumps(self.get_variables(id)),
            "extensions": json.dumps(self.__get_extensions())
        }

        response = await self.__client.get(SPOTIFY_PARTNER_URL + "/pathfinder/v1/query", params=params, headers=self.__headers)
        res_json = await response.json()
        return res_json

