from .gql_query import GQLQuery
from datetime import datetime

GQL_GET_ALBUM_STR = \
"""
query getAlbum($uri: ID!, $locale: String, $offset: Int, $limit: Int) {
  albumUnion(uri: $uri) {
    __typename
    ... on Album {
      ...albumMetadataFull
    }
  }
}

fragment albumMetadataFull on Album {
  uri
  name
  ...albumArtists
  ...albumCoverArt
  ...albumDiscs
  ...albumReleases
  type
  date {
    isoString
    precision
  }
  playability {
    playable
    reason
  }
  label
  copyright {
    totalCount
    items {
      type
      text
    }
  }
  courtesyLine
  saved
  sharingInfo(customData: [{key: "wpi", value: $locale}]) {
    shareUrl
    shareId
  }
  tracks(offset: $offset, limit: $limit) {
    totalCount
    items {
      ...albumTrack
    }
  }
  ...moreAlbumsByArtist
}

fragment albumArtists on Album {
  artists {
    totalCount
    items {
      id
      uri
      profile {
        name
      }
      visuals {
        avatarImage {
          sources {
            url
            width
            height
          }
        }
      }
      sharingInfo(customData: [{key: "wpi", value: $locale}]) {
        shareUrl
      }
    }
  }
}

fragment albumCoverArt on Album {
  coverArt {
    extractedColors {
      colorRaw {
        hex
      }
      colorLight {
        hex
      }
      colorDark {
        hex
      }
    }
    sources {
      url
      width
      height
    }
  }
}

fragment albumDiscs on Album {
  discs {
    totalCount
    items {
      number
      tracks {
        totalCount
      }
    }
  }
}

fragment albumReleases on Album {
  releases {
    totalCount
    items {
      uri
      name
    }
  }
}

fragment albumTrack on ContextTrack {
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
      linkedTrack {
        __typename
        ... on Track {
          uri
        }
      }
    }
    duration {
      totalMilliseconds
    }
    playability {
      playable
    }
    artists(offset: 0, limit: 20) {
      items {
        uri
        profile {
          name
        }
      }
    }
  }
}

fragment moreAlbumsByArtist on Album {
  moreAlbumsByArtist: artists(limit: 1) {
    items {
      discography {
        popularReleasesAlbums(limit: 10) {
          items {
            id
            uri
            name
            date {
              year
            }
            coverArt {
              sources {
                url
                width
                height
              }
            }
            playability {
              playable
              reason
            }
            sharingInfo(customData: [{key: "wpi", value: $locale}]) {
              shareId
              shareUrl
            }
            type
          }
        }
      }
    }
  }
}

"""[1:-1]


class AlbumPlayCount(GQLQuery):
    name: str = "getAlbum"
    endpoint: str = "/albumPlayCount"
    gql_query: str = GQL_GET_ALBUM_STR

    def get_variables(self, id: str) -> dict:
        return {
            "uri": "spotify:album:" + id,
            "locale": "",
            "offset": 0,
            "limit": 50
        }
    
    def parse_response(self, response_json: dict) -> dict:
        response_json = response_json["data"]["albumUnion"]

        uri = response_json["uri"]
        name = response_json["name"]
        cover = { "uri": response_json["coverArt"]["sources"][0]["url"] }
        date = datetime.strptime(response_json["date"]["isoString"], "%Y-%m-%dT%H:%M:%SZ")
        year = date.year
        month = date.month
        day = date.day
        track_count = response_json["tracks"]["totalCount"]
        artists = [
            {
                "name": artist["profile"]["name"],
                "uri": "spotify:artist:" + artist["id"],
                "image": { "uri": "" } # Not implemented
            } for artist in response_json["artists"]["items"]
        ]
        discs = [
            {
                "number": disc["number"],
                "name": name,
                "tracks": [
                    {
                        "uri": track["track"]["uri"],
                        "playcount": int(track["track"]["playcount"]),
                        "name": track["track"]["name"],
                        "popularity": 0, # Not implemented
                        "number": track["track"]["trackNumber"],
                        "duration": track["track"]["duration"]["totalMilliseconds"],
                        "explicit": track["track"]["contentRating"]["label"] == "EXPLICIT",
                        "playable": track["track"]["playability"]["playable"],
                        "artists": artists, # Not implemented
                    } for track in response_json["tracks"]["items"] if track["track"]["discNumber"] == disc["number"]
                ]
            } for disc in response_json["discs"]["items"]
        ]
        related = { "releases": [] } # Not implemented
        copyrights = [ copyright["text"] for copyright in response_json["copyright"]["items"] ]
        label = response_json["label"]
        album_type = response_json["type"]

        return {
            "uri": uri,
            "name": name,
            "cover": cover,
            "year": year,
            "month": month,
            "day": day,
            "track_count": track_count,
            "discs": discs,
            "copyrights": copyrights,
            "artists": artists,
            "related": related,
            "type": album_type,
            "label": label
        }
        