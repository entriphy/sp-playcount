from .gql_query import GQLQuery

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


class GetAlbum(GQLQuery):
    name: str = "getAlbum"
    endpoint: str = "/getAlbum"
    gql_query: str = GQL_GET_ALBUM_STR

    def get_variables(self, id: str) -> dict:
        return {
            "uri": "spotify:album:" + id,
            "locale": "",
            "offset": 0,
            "limit": 50
        }
    