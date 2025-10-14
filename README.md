# sp-playcount
Proxy for Spotify's partner API to retrieve extra statistics not provided in the public web API.

## Disclaimer
This project is to be used for educational purposes only. I do not condone using this tool for commercial purposes. Doing so puts this project at risk and can cause legal issues (the data is property of Spotify, not me). Any attempt or request to pay me for anything related to this project will be denied.

## Running
1. Copy or rename `wrangler.jsonc.example` to `wrangler.jsonc`. If deploying to Cloudflare, edit the KV ID in this config file.
2. Run the following commands:
```bash
npm install
npm run dev
```

## Secrets
[As of October 10th, 2025](https://github.com/librespot-org/librespot/discussions/1562), secrets required for authentication will not be provided in this repository. A URL to a raw JSON file containing a list of secrets with the following format must be provided:
```ts
interface SpotifySecret {
  version: number;
  secret: number[];
};
```
The secrets URL can be set using the following command:
```bash
npx wrangler kv key put --binding=KV secrets_url <url>
```
A certain [horse](https://umamusume.jp/character/haruurara) may help you out with this one. 🐴

## Endpoints
All endpoints take `id` as a query parameter, where `id` is either an album ID or an artist ID. (e.g. [`/getAlbum?id=4P5WTqxveCHwel30kXJvoo`](https://api.t4ils.dev/getAlbum?id=4P5WTqxveCHwel30kXJvoo)) Some endpoints have a legacy endpoint to provide backwards-compatibility with Spotify's old Hermes API response.
* `/getAlbum` (Legacy: `/albumPlayCount`)
* `/getAlbumTracks`
* `/getArtist` (Legacy: `/artistInsights`)

