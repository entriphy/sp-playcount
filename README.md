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

## Endpoints
All endpoints take `id` as a query parameter, where `id` is either an album ID or an artist ID. (e.g. [`/getAlbum?id=4P5WTqxveCHwel30kXJvoo`](https://api.t4ils.dev/getAlbum?id=4P5WTqxveCHwel30kXJvoo)) Some endpoints have a legacy endpoint to provide backwards-compatibility with Spotify's old Hermes API response.
* `/getAlbum` (Legacy: `/albumPlayCount`)
* `/getAlbumTracks`
* `/getArtist` (Legacy: `/artistInsights`)

