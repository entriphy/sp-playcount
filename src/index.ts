import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { cache } from 'hono/cache';
import { GetAlbumQuery, OldGetAlbumQuery } from './queries/album';
import { GetAlbumTracksQuery } from './queries/track';
import { GetArtistInsights, GetArtistQuery } from './queries/artist';
import { spotifyRequest } from './spotify';

const app = new Hono<{ Bindings: CloudflareBindings }>()

app.use("/:query", cors());
app.use("/:query", cache({cacheName: "cache", cacheControl: "max-age=21600"}))
app.get("/:query", async (c) => {
  const id = c.req.query("id") || c.req.query("albumid") || c.req.query("artistid");
  if (id === undefined) {
    return c.json({success: false, data: "id is not defined in the query"}, 400);
  } else if (id.length != 22) {
    return c.json({success: false, data: "id must have a length of 22 characters"}, 400);
  }

  const queries = [
    new GetAlbumQuery(id),
    new OldGetAlbumQuery(id),
    new GetAlbumTracksQuery(id),
    new GetArtistQuery(id),
    new GetArtistInsights(id)
  ];

  const userQuery = c.req.param("query");
  const query = queries.find(query => query.endpoint === userQuery);
  if (query === undefined) {
    return c.json({success: false, data: `Query not found: ${userQuery}`}, 404);
  }

  try {
    const response = await spotifyRequest(c.env.KV, query);
    const union = response.data.artistUnion || response.data.albumUnion;
    if (union === undefined || union.__typename === "NotFound") {
      return c.json({success: false, data: `id not found: ${id}`}, 404)
    }

    try {
      const parsed = query.parseResponse(response);
      return c.json({success: true, data: parsed});
    } catch (e) {
      return c.json({success: false, data: `Error when parsing response: ${e}`}, 500)
    }
  } catch (e) {
    return c.json({success: false, data: `An unknown error occurred: ${e}`}, 500);
  }
});

export default app;
