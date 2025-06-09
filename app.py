from aiohttp import web, ClientSession
from aiocache import cached, Cache
import base64
import pyotp
import queries
from queries.gql_query import GQLQuery
import time
from datetime import datetime
import typing

SPOTIFY_WEB_URL = "https://open.spotify.com"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
DEFAULT_RESPONSE_HEADERS = {
    "Access-Control-Allow-Origin": "*"
}
CIPHER = [12, 56, 76, 33, 88, 44, 88, 33, 78, 78, 11, 66, 22, 22, 55, 69, 54]
PROCESSED_CIPHER = "".join(str(c ^ (i % 33 + 9)) for i, c in enumerate(CIPHER))
CIPHER_BYTES = PROCESSED_CIPHER.encode("ascii")


class App:
    app: web.Application
    client: ClientSession
    headers: dict
    client_id: str
    access_token_expiration: int
    queries_map: typing.Dict[str, GQLQuery]

    def __init__(self):
        self.app = web.Application()
        self.client = ClientSession()
        self.headers = {
            "accept": "application/json",
            "app-platform": "WebPlayer",
            "content-type": "application/json",
            "origin": SPOTIFY_WEB_URL,
            "referer": SPOTIFY_WEB_URL + "/",
            "user-agent": USER_AGENT
        }

        # this is cringe
        self.queries_map = { query.endpoint: query(self.client, self.headers) for query in GQLQuery.__subclasses__() }
        self.app.add_routes([web.get(query.endpoint, self.handle_request) for query in GQLQuery.__subclasses__()])


    async def handle_request(self, request: web.Request):
        path = request.path
        if path not in self.queries_map:
            return web.json_response({"success": False, "data": "Invalid endpoint " + path}, status=400, headers=DEFAULT_RESPONSE_HEADERS)
        id = request.query.get("id", request.query.get("albumid", request.query.get("artistid")))
        if id == None:
            return web.json_response({"success": False, "data": "id is not defined in the query"}, status=400, headers=DEFAULT_RESPONSE_HEADERS)
        if len(id) != 22:
            return web.json_response({"success": False, "data": "id must have a length of 22 characters"}, status=400, headers=DEFAULT_RESPONSE_HEADERS)
        
        try:
            response = await self.do_query(path, id)
            return web.json_response({"success": True, "data": response}, status=200, headers=DEFAULT_RESPONSE_HEADERS)
        except (QueryError, ParseError) as e:
            return web.json_response({"success": False, "data": str(e)}, status=500, headers=DEFAULT_RESPONSE_HEADERS)
        except NotFoundError as e:
            return web.json_response({"success": False, "data": str(e)}, status=404, headers=DEFAULT_RESPONSE_HEADERS)
        except Exception as e:
            return web.json_response({"success": False, "data": "An unknown error occurred: " + str(e)}, status=500, headers=DEFAULT_RESPONSE_HEADERS)
    
    
    @cached(ttl=6*60*60, cache=Cache.MEMORY)
    async def do_query(self, path, id) -> dict:
        query = self.queries_map[path]

        try:
            response = await query.send_query(id)
        except Exception as e:
            raise QueryError("Error while querying: " + str(e))
        
        union = response["data"].get("artistUnion", response["data"].get("albumUnion"))
        if union == None or union["__typename"] == "NotFound":
            raise NotFoundError("id not found: " + id)

        try:
            parsed_response = query.parse_response(response)
            return parsed_response
        except Exception as e:
            raise ParseError("Error while parsing response: " + str(e))


    async def refresh_token(self):
        # Get TOTP (see issue #3)
        secret = base64.b32encode(CIPHER_BYTES).decode("ascii").strip("=")
        totp = pyotp.TOTP(secret).at(datetime.now())

        # Get access token
        params = {
            "reason": "transport",
            "productType": "web-player",
            "totp": totp,
            "totpVer": 5,
        }
        response = await self.client.get("https://open.spotify.com/api/token", params=params)
        access_token_json = await response.json()
        self.headers["authorization"] = "Bearer " + access_token_json["accessToken"]
        self.client_id = access_token_json["clientId"]
        self.access_token_expiration = access_token_json["accessTokenExpirationTimestampMs"]
    

    async def cleanup(self):
        await self.client.close()


class QueryError(Exception):
    ...


class ParseError(Exception):
    ...


class NotFoundError(Exception):
    ...
