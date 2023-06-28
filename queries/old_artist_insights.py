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

class ArtistInsights(GQLQuery):
    name: str = "queryArtistOverview"
    endpoint: str = "/artistInsights"
    gql_query: str = GQL_QUERY_ARTIST_OVERVIEW_STR

    def get_variables(self, id: str) -> dict:
        return {
            "uri": "spotify:artist:" + id,
            "locale": "",
            "includePrerelease": "true"
        }

    def parse_response(self, response_json: dict) -> dict:
        response_json = response_json["data"]["artistUnion"]

        artist_gid = "" # Not implemented
        artist_name = response_json["profile"]["name"]
        main_image_url = response_json["visuals"]["avatarImage"]["sources"][0]["url"]
        header_image = {
            "id": "", # Not implemented
            "uri": response_json["visuals"]["headerImage"]["sources"][0]["url"],
            "width": response_json["visuals"]["headerImage"]["sources"][0]["width"],
            "height": response_json["visuals"]["headerImage"]["sources"][0]["height"]
        } if response_json["visuals"]["headerImage"] != None else None
        autobiography = { "body": response_json["profile"]["biography"]["text"] }
        links = { link["name"]: link["url"] for link in response_json["profile"]["externalLinks"]["items"] }
        images = [
            {
                "id": "", # Not implemented
                "uri": image["sources"][0]["url"],
                "width": image["sources"][0]["width"],
                "height": image["sources"][0]["height"],
            } for image in response_json["visuals"]["gallery"]["items"]
        ]
        images_count = len(images)
        global_chart_position = response_json["stats"]["worldRank"]
        monthly_listeners = response_json["stats"]["monthlyListeners"]
        monthly_listeners_delta = 0 # Not implemented
        follower_count = response_json["stats"]["followers"]
        following_count = 0 # Not implemented
        playlists = {
            "entries": [
                {
                    "uri": playlist["data"]["uri"],
                    "name": playlist["data"]["name"],
                    "imageUrl": playlist["data"]["images"]["items"][0]["sources"][0]["url"],
                    "owner": {
                        "name": playlist["data"]["ownerV2"]["data"]["name"],
                        "uri": "" # Not implemented
                    },
                    "listeners": 0 # Not implemented
                } for playlist in response_json["relatedContent"]["discoveredOnV2"]["items"] if playlist["data"]["__typename"] != "NotFound"
            ]
        }
        cities = [
            {
                "country": city["country"],
                "region": city["region"],
                "city": city["city"],
                "listeners": city["numberOfListeners"]
            } for city in response_json["stats"]["topCities"]["items"]
        ]

        return {
            "artistGid": artist_gid,
            "name": artist_name,
            "mainImageUrl": main_image_url,
            "headerImage": header_image,
            "autobiography": autobiography,
            "links": links,
            "biography": "",
            "images": images,
            "imagesCount": images_count,
            "globalChartPosition": global_chart_position,
            "monthlyListeners": monthly_listeners,
            "monthlyListenersDelta": monthly_listeners_delta,
            "followerCount": follower_count,
            "followingCount": following_count,
            "playlists": playlists,
            "cities": cities
        }