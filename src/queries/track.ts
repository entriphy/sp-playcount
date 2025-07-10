import GQLQuery, { JSONRecord } from "../query";

const GET_TRACKS_QUERY = `query queryAlbumTracks($uri: ID!, $offset: Int, $limit: Int) {
  album(uri: $uri) {
    playability {
      playable
    }
    tracks(offset: $offset, limit: $limit) {
      totalCount
      items {
        uid
        track {
          saved
          uri
          name
          playcount
          discNumber
          trackNumber
          contentRating {
            label
          }
          relinkingInformation {
            uri
            isRelinked
          }
          duration {
            totalMilliseconds
          }
          playability {
            playable
          }
          artists(offset: 0, limit: 10) {
            items {
              uri
              profile {
                name
              }
            }
          }
        }
      }
    }
  }
}
`

export class GetAlbumTracksQuery extends GQLQuery {
    name: string = "queryAlbumTracks";
    query: string = GET_TRACKS_QUERY;
    endpoint: string = "getAlbumTracks"

    get variables(): JSONRecord {
        return {
            uri: `spotify:album:${this.id}`,
            offset: 0,
            limit: 50
        }
    }
}