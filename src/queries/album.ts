import GQLQuery, { JSONRecord } from "../query";

const GET_ALBUM_QUERY = `query getAlbum($uri: ID!, $locale: String, $offset: Int, $limit: Int) {
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
`;

export class GetAlbumQuery extends GQLQuery {
    name: string = "getAlbum";
    query: string = GET_ALBUM_QUERY;
    endpoint: string = "getAlbum"

    get variables(): JSONRecord {
        return {
            uri: `spotify:album:${this.id}`,
            locale: "",
            offset: 0,
            limit: 50
        }
    }
}

export class OldGetAlbumQuery extends GetAlbumQuery {
    endpoint: string = "albumPlayCount"

    public parseResponse(json: JSONRecord): JSONRecord {
        const responseJson = json.data.albumUnion;
        const uri = responseJson.uri;
        const name = responseJson.name;
        const cover = { uri: responseJson.coverArt.sources[0].url };
        const date = new Date(responseJson.date.isoString);
        const year = date.getUTCFullYear();
        const month = date.getUTCMonth();
        const day = date.getUTCDate();
        const trackCount = responseJson.tracks.totalCount;
        const artists = responseJson.artists.items.map((artist: { profile: { name: any; }; id: string; }) => (
            {
                name: artist.profile.name,
                uri: "spotify:artist:" + artist.id,
                image: { uri: ""} // Not implemented
            }
        ));
        const discs = responseJson.discs.items.map((disc: { number: any; }) => ({
            number: disc.number,
            name: name,
            tracks: responseJson.tracks.items.filter((track: { track: { discNumber: any; }; }) => track.track.discNumber == disc.number).map((track: { track: { uri: any; playcount: string; name: any; trackNumber: any; duration: { totalMilliseconds: any; }; contentRating: { label: string; }; playability: { playable: any; }; }; }) => ({
                uri: track.track.uri,
                playcount: parseInt(track.track.playcount),
                name: track.track.name,
                popularity: 0, // Not implemented
                number: track.track.trackNumber,
                duration: track.track.duration.totalMilliseconds,
                explicit: track.track.contentRating.label === "EXPLICIT",
                playable: track.track.playability.playable,
                artists: artists, // Not implemented
            }))
        }));
        const related = { releases: [] }; // Not implemented
        const copyrights = responseJson.copyright.items.map((copyright: { text: any }) => copyright.text)
        const label = responseJson.label;
        const albumType = responseJson.type;

        return {
            uri: uri,
            name: name,
            cover: cover,
            year: year,
            month: month,
            day: day,
            track_count: trackCount,
            discs: discs,
            copyrights: copyrights,
            artists: artists,
            related: related,
            type: albumType,
            label: label
        }
    }
}