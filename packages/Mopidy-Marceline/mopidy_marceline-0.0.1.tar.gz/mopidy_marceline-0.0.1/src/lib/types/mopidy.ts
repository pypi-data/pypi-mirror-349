import type Mopidy from "mopidy";
import type { Branded } from "./brand";
import type { Override } from "./util";

export type PlaybackState = Mopidy.core.PlaybackState;

export type PlaylistURI = Branded<string, "PlaylistURI">;
export type ArtistURI = Branded<string, "ArtistURI">;
export type AlbumURI = Branded<string, "AlbumURI">;
export type TrackURI = Branded<string, "TrackURI">;
export type DirectoryURI = Branded<string, "DirectoryURI">;

export type ModelURI =
    | PlaylistURI
    | ArtistURI
    | AlbumURI
    | TrackURI
    | DirectoryURI;

export type Playlist = Override<
    Mopidy.models.Playlist,
    {
        uri: PlaylistURI;
        tracks: Track[];
    }
>;

export type Artist = Override<
    Mopidy.models.Artist,
    {
        uri: ArtistURI;
    }
>;

export type Album = Override<
    Mopidy.models.Album,
    {
        uri: AlbumURI;
        artists: Artist[];
    }
>;

export type Track = Override<
    Mopidy.models.Track,
    {
        uri: TrackURI;
        artists: Artist[];
        album: Album;
        composers: Artist[];
        performers: Artist[];
    }
>;

export type TlTrack = Override<
    Mopidy.models.TlTrack,
    {
        track: Track;
    }
>;

export type TrackLyrics = {
    timestamp: number;
    lyrics: string;
}[];
