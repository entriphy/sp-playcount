import base32Encode from "base32-encode";
import GQLQuery, { JSONRecord } from "./query";
import { TOTP } from "totp-generator";

const SPOTIFY_WEB_URL = "https://open.spotify.com"
const SPOTIFY_APP_VERSION = "1.2.68.438.ga33faf54" // This should probably be scraped from the web player
const USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
const SPOTIFY_PARTNER_URL = "https://api-partner.spotify.com";
const CIPHER = [59, 92, 64, 70, 99, 78, 117, 75, 99, 103, 116, 67, 103, 51, 87, 63, 93, 59, 70, 45, 32];
const PROCESSED_CIPHER = CIPHER.map((c, i) => (c ^ (i % 33 + 9)).toString()).join("")
const CIPHER_BYTES = Uint8Array.from(PROCESSED_CIPHER.split("").map(c => c.charCodeAt(0)))
const TOTP_VER = "13";

interface TokenResponse {
  clientId: string;
  accessToken: string;
  accessTokenExpirationTimestampMs: number;
  isAnonymous: boolean;
  _notes: string;
  totpVerExpired: string;
  totpValidUntil: string;
}

async function refreshToken(): Promise<TokenResponse> {
  const secret = base32Encode(CIPHER_BYTES, "RFC4648", { padding: false });
  const { otp } = TOTP.generate(secret);

  const url = new URL("/api/token", SPOTIFY_WEB_URL);
  url.searchParams.set("reason", "init");
  url.searchParams.set("productType", "web-player");
  url.searchParams.set("totp", otp);
  url.searchParams.set("totpVer", TOTP_VER);

  const response = await fetch(url, { method: "GET" });
  return response.json()
}

async function getToken(kv: KVNamespace<string>): Promise<string> {
  const token = await kv.get<TokenResponse>("token", "json");
  const date = new Date();
  if (token === null || date > new Date(token.accessTokenExpirationTimestampMs)) {
    const res = await refreshToken();
    if (res.accessToken === undefined) {
      throw new Error("Failed to refresh access token");
    }
    await kv.put("token", JSON.stringify(res));
    return res.accessToken;
  } else {
    return token.accessToken;
  }
}

export async function spotifyRequest(kv: KVNamespace<string>, query: GQLQuery): Promise<JSONRecord> {
  const token = await getToken(kv);

  const url = new URL("/pathfinder/v1/query", SPOTIFY_PARTNER_URL);
  url.searchParams.set("operationName", query.name);
  url.searchParams.set("variables", JSON.stringify(query.variables));
  url.searchParams.set("extensions", JSON.stringify(await query.getExtensions()));

  const headers = {
    "accept": "application/json",
    "app-platform": "WebPlayer",
    "content-type": "application/json",
    "origin": SPOTIFY_WEB_URL,
    "referer": SPOTIFY_WEB_URL + "/",
    "spotify-app-version": SPOTIFY_APP_VERSION,
    "user-agent": USER_AGENT,
    "authorization": "Bearer " + token
  };

  const response = await fetch(url, { method: "GET", headers: headers });
  return await response.json()
}