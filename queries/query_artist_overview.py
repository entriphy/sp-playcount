from .gql_query import GQLQuery

GQL_QUERY_ARTIST_OVERVIEW_STR = \
"""
query queryArtistOverview($uri: ID!, $locale: String, $includePrerelease: Boolean!) {
  artistUnion(uri: $uri) {
    __typename
    ... on Artist {
      id
      uri
      saved
      sharingInfo(customData: [{key: "wpi", value: $locale}]) {
        shareUrl
        shareId
      }
      preRelease @include(if: $includePrerelease) {
        ...artistOverviewPrerelease
      }
      profile {
        name
        verified
        pinnedItem {
          comment
          type
          backgroundImage {
            sources {
              url
            }
          }
          itemV2 {
            ... on MerchResponseWrapper {
              data(utmContent: "direct", utmMedium: "app-artistpick") {
                ... on Merch {
                  uri
                  name
                  price
                  url
                  image {
                    sources {
                      height
                      width
                      url
                    }
                  }
                }
              }
            }
          }
          item {
            ... on ExclusiveMerch {
              uri
              title
              subtitle
              checkoutUrl
            }
            ... on Artist {
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
            }
            ... on Playlist {
              uri
              name
              images {
                items {
                  sources {
                    url
                    width
                    height
                  }
                }
              }
            }
            ... on Album {
              uri
              name
              coverArt {
                sources {
                  url
                  width
                  height
                }
              }
              type
            }
            ... on Concert {
              uri
              title
              id
              date {
                isoString
              }
              venue {
                name
                location {
                  name
                }
              }
            }
            ... on Track {
              uri
              name
              albumOfTrack {
                coverArt {
                  sources {
                    url
                    width
                    height
                  }
                }
              }
            }
            ... on Episode {
              uri
              name
              coverArt {
                sources {
                  height
                  width
                  url
                }
              }
            }
          }
        }
        biography {
          type
          text
        }
        externalLinks {
          items {
            ...artistExternalLinkItem
          }
        }
        playlistsV2(offset: 0, limit: 10) {
          totalCount
          items {
            data {
              __typename
              ... on Playlist {
                uri
                name
                description
                ownerV2 {
                  data {
                    __typename
                    ... on User {
                      name
                    }
                  }
                }
                images(limit: 1) {
                  items {
                    sources {
                      url
                      width
                      height
                    }
                  }
                }
              }
            }
          }
        }
      }
      visuals {
        gallery(offset: 0, limit: 25) {
          items {
            sources {
              url
              width
              height
            }
          }
        }
        avatarImage {
          sources {
            url
            width
            height
          }
          extractedColors {
            colorRaw {
              hex
            }
          }
        }
        headerImage {
          sources {
            url
            width
            height
          }
          extractedColors {
            colorRaw {
              hex
            }
          }
        }
      }
      discography {
        ...artistDiscography
      }
      stats {
        followers
        monthlyListeners
        worldRank
        topCities {
          items {
            ...artistTopCity
          }
        }
      }
      relatedContent {
        appearsOn(limit: 20) {
          totalCount
          items {
            releases(offset: 0, limit: 20) {
              totalCount
              items {
                uri
                id
                name
                type
                artists(limit: 1) {
                  items {
                    uri
                    profile {
                      name
                    }
                  }
                }
                coverArt {
                  sources {
                    url
                    width
                    height
                  }
                }
                date {
                  year
                }
                sharingInfo(customData: [{key: "wpi", value: $locale}]) {
                  shareId
                  shareUrl
                }
              }
            }
          }
        }
        featuringV2(limit: 20) {
          totalCount
          items {
            data {
              __typename
              ... on Playlist {
                uri
                id
                ownerV2 {
                  data {
                    __typename
                    ... on User {
                      name
                    }
                  }
                }
                name
                description
                images {
                  totalCount
                  items {
                    sources {
                      url
                      width
                      height
                    }
                  }
                }
              }
            }
          }
        }
        discoveredOnV2(limit: 20) {
          totalCount
          items {
            data {
              __typename
              ... on Playlist {
                uri
                id
                ownerV2 {
                  data {
                    __typename
                    ... on User {
                      name
                    }
                  }
                }
                name
                description
                images {
                  totalCount
                  items {
                    sources {
                      url
                      width
                      height
                    }
                  }
                }
              }
            }
          }
        }
        relatedArtists(limit: 20) {
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
          }
        }
      }
      goods {
        events {
          userLocation {
            name
          }
          concerts(offset: 0, limit: 10) {
            totalCount
            items {
              uri
              id
              title
              category
              festival
              nearUser
              venue {
                name
                location {
                  name
                }
                coordinates {
                  latitude
                  longitude
                }
              }
              artists(offset: 0, limit: 10) {
                items {
                  uri
                  id
                  profile {
                    name
                  }
                }
              }
              partnerLinks {
                items {
                  partnerName
                  url
                }
              }
              date {
                year
                month
                day
                hour
                minute
                second
                isoString
                precision
              }
            }
            pagingInfo {
              limit
            }
          }
        }
        merch(offset: 0, limit: 4) {
          items {
            ...artistMerchItem
          }
        }
      }
    }
  }
}

fragment artistOverviewPrerelease on PreRelease {
  uri
  releaseDate {
    isoString
  }
  preReleaseContent {
    name
    type
    coverArt {
      sources {
        url
        height
        width
      }
    }
  }
}

fragment artistExternalLinkItem on Link {
  name
  url
}

fragment artistDiscography on ArtistDiscography {
  latest {
    id
    uri
    name
    type
    copyright {
      items {
        type
        text
      }
    }
    date {
      year
      month
      day
      precision
    }
    coverArt {
      sources {
        url
        width
        height
      }
    }
    tracks {
      totalCount
    }
    label
    playability {
      playable
      reason
    }
    sharingInfo(customData: [{key: "wpi", value: $locale}]) {
      shareId
      shareUrl
    }
  }
  popularReleasesAlbums(offset: 0, limit: 10) {
    totalCount
    items {
      id
      uri
      name
      type
      copyright {
        items {
          type
          text
        }
      }
      date {
        year
        month
        day
        precision
      }
      coverArt {
        sources {
          url
          width
          height
        }
      }
      tracks {
        totalCount
      }
      label
      playability {
        playable
        reason
      }
      sharingInfo(customData: [{key: "wpi", value: $locale}]) {
        shareId
        shareUrl
      }
    }
  }
  singles(offset: 0, limit: 10) {
    totalCount
    items {
      releases(limit: 1) {
        items {
          id
          uri
          name
          type
          copyright {
            items {
              type
              text
            }
          }
          date {
            year
            month
            day
            precision
          }
          coverArt {
            sources {
              url
              width
              height
            }
          }
          tracks {
            totalCount
          }
          label
          playability {
            playable
            reason
          }
          sharingInfo(customData: [{key: "wpi", value: $locale}]) {
            shareId
            shareUrl
          }
        }
      }
    }
  }
  albums(offset: 0, limit: 10) {
    totalCount
    items {
      releases(limit: 1) {
        items {
          id
          uri
          name
          type
          copyright {
            items {
              type
              text
            }
          }
          date {
            year
            month
            day
            precision
          }
          coverArt {
            sources {
              url
              width
              height
            }
          }
          tracks {
            totalCount
          }
          label
          playability {
            playable
            reason
          }
          sharingInfo(customData: [{key: "wpi", value: $locale}]) {
            shareId
            shareUrl
          }
        }
      }
    }
  }
  compilations(offset: 0, limit: 10) {
    totalCount
    items {
      releases(limit: 1) {
        items {
          id
          uri
          name
          type
          copyright {
            items {
              type
              text
            }
          }
          date {
            year
            month
            day
            precision
          }
          coverArt {
            sources {
              url
              width
              height
            }
          }
          tracks {
            totalCount
          }
          label
          playability {
            playable
            reason
          }
          sharingInfo(customData: [{key: "wpi", value: $locale}]) {
            shareId
            shareUrl
          }
        }
      }
    }
  }
  topTracks(offset: 0, limit: 10) {
    items {
      uid
      track {
        id
        uri
        name
        playcount
        discNumber
        duration {
          totalMilliseconds
        }
        playability {
          playable
          reason
        }
        contentRating {
          label
        }
        artists {
          items {
            uri
            profile {
              name
            }
          }
        }
        albumOfTrack {
          uri
          coverArt {
            sources {
              url
            }
          }
        }
      }
    }
  }
}

fragment artistTopCity on CityListenerStats {
  numberOfListeners
  city
  country
  region
}

fragment artistMerchItem on Merch {
  image {
    sources {
      url
    }
  }
  name
  description
  price
  uri
  url
}

"""[1:-1]

class QueryArtistOverview(GQLQuery):
    name: str = "queryArtistOverview"
    endpoint: str = "/getArtist"
    gql_query: str = GQL_QUERY_ARTIST_OVERVIEW_STR

    def get_variables(self, id: str) -> dict:
        return {
            "uri": "spotify:artist:" + id,
            "locale": "",
            "includePrerelease": True
        }
    