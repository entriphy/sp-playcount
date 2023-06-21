from aiohttp import web, ClientSession
from async_lru import alru_cache
import queries
from queries.gql_query import GQLQuery
import time

SPOTIFY_WEB_URL = "https://open.spotify.com"
SPOTIFY_APP_VERSION = "1.2.15.275.g634be5e0" # This should probably be scraped from the web player
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"

class App:
    app: web.Application
    client: ClientSession
    headers: dict
    client_id: str
    access_token_expiration: int
    queries_map: dict[str, GQLQuery]

    def __init__(self):
        self.app = web.Application()
        self.client = ClientSession()
        self.headers = {
            "accept": "application/json",
            "app-platform": "WebPlayer",
            "content-type": "application/json",
            "origin": SPOTIFY_WEB_URL,
            "referer": SPOTIFY_WEB_URL + "/",
            "spotify-app-version": SPOTIFY_APP_VERSION,
            "user-agent": USER_AGENT
        }

        # this is cringe
        self.queries_map = { query.endpoint: query(self.client, self.headers) for query in GQLQuery.__subclasses__() }
        self.app.add_routes([web.get(query.endpoint, self.handle_request) for query in GQLQuery.__subclasses__()])


    async def handle_request(self, request: web.Request):
        path = request.path
        if path not in self.queries_map:
            return web.json_response({"error": "Invalid endpoint " + path}, status=400)
        if "id" not in request.query:
            return web.json_response({"error": "id is not defined in the query"}, status=400)
        id = request.query["id"]
        if len(id) != 22:
            return web.json_response({"error": "id must have a length of 22 characters"}, status=400)
        response = await self.do_query(path, id)
        return web.json_response(response)
    
    
    @alru_cache(maxsize=1024, ttl=60*60*6)
    async def do_query(self, path, id) -> dict:
        query = self.queries_map[path]
        response = await query.send_query(id)
        return response


    async def refresh_token(self):
        response = await self.client.get("https://open.spotify.com/get_access_token", params={"reason": "transpost", "productType": "web_player"})
        access_token_json = await response.json()

        self.headers["authorization"] = "Bearer " + access_token_json["accessToken"]
        self.client_id = access_token_json["clientId"]
        self.access_token_expiration = access_token_json["accessTokenExpirationTimestampMs"]
    

    async def cleanup(self):
        await self.client.close()
