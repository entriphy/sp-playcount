from .gql_query import GQLQuery

GQL_QUERY_ALBUM_TRACKS_STR = \
"""
query queryAlbumTracks($uri: ID!, $offset: Int, $limit: Int) {
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

"""[1:-1]


class QueryAlbumTracks(GQLQuery):
    name: str = "queryAlbumTracks"
    endpoint: str = "/getAlbumTracks"
    gql_query: str = GQL_QUERY_ALBUM_TRACKS_STR

    def get_variables(self, id: str) -> dict:
        return {
            "uri": "spotify:album:" + id,
            "offset": 0,
            "limit": 50
        }
    