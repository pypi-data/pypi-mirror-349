import { BASE_URL, WS_URL } from "$lib/constants";
import { themeFromImage } from "@material/material-color-utilities";
import Mopidy from "mopidy";
import { SvelteMap } from "svelte/reactivity";
import * as lrclib from "$lib/lrclib";
import type {
    Album,
    AlbumURI,
    Artist,
    ArtistURI,
    ModelURI,
    PlaybackState,
    PlaylistURI,
    TlTrack,
    Track,
    TrackLyrics,
    TrackURI,
} from "$lib/types/mopidy";
import { brand } from "$lib/types/brand";

class MopidyState {
    base: Mopidy;

    // Tracklist

    #queue = $state<TlTrack[]>([]);
    get queue() {
        return this.#queue;
    }
    async #updateQueue() {
        if (!this.base.tracklist) return;

        try {
            this.#queue =
                (await this.base.tracklist.getTlTracks()) as TlTrack[];
        } catch (e: unknown) {
            console.error("Failed to get queue");
            console.error(e);
        }
    }

    #consume = $state(false);
    get consume() {
        return this.#consume;
    }
    set consume(value: boolean) {
        void this.base.tracklist?.setConsume({ value });
    }
    async #updateConsume() {
        if (!this.base.tracklist) return;

        try {
            this.#consume = await this.base.tracklist.getConsume();
        } catch (e: unknown) {
            console.error("Failed to get consume");
            console.error(e);
        }
    }

    #shuffle = $state(false);
    get shuffle() {
        return this.#shuffle;
    }
    set shuffle(value: boolean) {
        void this.base.tracklist?.setRandom({ value });
    }
    async #updateShuffle() {
        if (!this.base.tracklist) return;

        try {
            this.#shuffle = await this.base.tracklist.getRandom();
        } catch (e: unknown) {
            console.error("Failed to get shuffle");
            console.error(e);
        }
    }

    #repeat = $state(false);
    get repeat() {
        return this.#repeat;
    }
    set repeat(value: boolean) {
        void this.base.tracklist?.setRepeat({ value });
    }
    async #updateRepeat() {
        if (!this.base.tracklist) return;

        try {
            this.#repeat = await this.base.tracklist.getRepeat();
        } catch (e: unknown) {
            console.error("Failed to get repeat");
            console.error(e);
        }
    }

    #single = $state(false);
    get single() {
        return this.#single;
    }
    set single(value: boolean) {
        void this.base.tracklist?.setSingle({ value });
    }
    async #updateSingle() {
        if (!this.base.tracklist) return;

        try {
            this.#single = await this.base.tracklist.getSingle();
        } catch (e: unknown) {
            console.error("Failed to get single");
            console.error(e);
        }
    }

    // Playback

    #currentTrack = $state<TlTrack | null>(null);
    get currentTrack() {
        return this.#currentTrack;
    }
    async #updateCurrentTrack() {
        if (!this.base.playback) return;

        try {
            await this.#setCurrentTrack(
                (await this.base.playback.getCurrentTlTrack()) as TlTrack,
            );
        } catch (e: unknown) {
            console.error("Failed to get current track");
            console.error(e);
        }
    }
    async #setCurrentTrack(track: TlTrack | null) {
        this.#currentTrack = track;

        if (track)
            try {
                const lyricPromise = this.requestLyrics(track.track);

                const image = (await this.requestImages([track.track.uri]))?.at(
                    0,
                );

                if (image) await this.requestPalette(image);

                await lyricPromise;
            } catch (e: unknown) {
                console.error("Failed to get image, palette, or lyrics");
                console.error(e);
            }
    }

    #timePosition = $state<number | null>(null);
    get timePosition() {
        return this.#timePosition;
    }
    set timePosition(timePosition: number | null) {
        if (timePosition !== null)
            void this.base.playback?.seek({ time_position: timePosition });
    }
    async #updateTimePosition() {
        if (!this.base.playback) return;

        try {
            this.#timePosition = await this.base.playback.getTimePosition();
        } catch (e: unknown) {
            console.error("Failed to get time position");
            console.error(e);
        }
    }

    #playbackState = $state<PlaybackState>("stopped");
    get playbackState() {
        return this.#playbackState;
    }
    set playbackState(playbackState: PlaybackState) {
        switch (playbackState) {
            case "playing":
                void this.base.playback?.resume();
                break;
            case "paused":
                void this.base.playback?.pause();
                break;
            case "stopped":
                void this.base.playback?.stop();
                break;
            default:
                console.error("Unknown playback state");
                break;
        }
    }
    async #updatePlaybackState() {
        if (!this.base.playback) return;

        try {
            this.#playbackState = await this.base.playback.getState();
        } catch (e: unknown) {
            console.error("Failed to get playback state");
            console.error(e);
        }
    }

    togglePlaybackState() {
        switch (this.playbackState) {
            case "playing":
                this.playbackState = "paused";
                break;
            case "paused":
                this.playbackState = "playing";
                break;
            case "stopped":
                break;
            default:
                console.error("Unknown playback state");
                break;
        }
    }

    skipPrevious() {
        void this.base.playback?.previous();
    }

    skipNext() {
        void this.base.playback?.next();
    }

    // Library

    #artists = new SvelteMap<ArtistURI, Artist[]>();

    getArtist(uri: ArtistURI) {
        return this.#artists.get(uri);
    }

    async requestArtists(uris: ArtistURI[]) {
        // TODO
    }

    #albums = new SvelteMap<AlbumURI, Album[]>();

    getAlbum(uri: AlbumURI) {
        return this.#albums.get(uri);
    }

    async requestAlbums(uris: AlbumURI[]) {
        // TODO
    }

    #tracks = new SvelteMap<TrackURI, Track[]>();

    getTrack(uri: TrackURI) {
        return this.#tracks.get(uri);
    }

    async requestTracks(uris: TrackURI[]) {
        // TODO
    }

    #images = new SvelteMap<ModelURI, string>();

    getImage(uri: ModelURI) {
        return this.#images.get(uri);
    }

    #currentTrackImage: string | null = $derived(
        this.#currentTrack
            ? (this.getImage(this.#currentTrack.track.uri) ?? null)
            : null,
    );
    get currentTrackImage() {
        return this.#currentTrackImage;
    }

    async requestImages(uris: ModelURI[]) {
        try {
            const images =
                (await this.base.library?.getImages({
                    uris: uris.filter(
                        (uri) => !this.#images.has(uri),
                    ) as string[],
                })) ?? {};

            for (const [uri, imageList] of Object.entries(images)) {
                const image = imageList.at(0);

                if (!image) continue;

                const url = new URL(image.uri, BASE_URL).toString();
                this.#images.set(uri as ModelURI, url);
            }

            return uris.map((uri) => this.#images.get(uri));
        } catch (e) {
            console.error("Failed to get images");
            console.error(e);
        }
    }

    // Playlists

    #playlists = $state<PlaylistURI[]>([]);
    get playlists() {
        return this.#playlists;
    }
    async #updatePlaylists() {
        if (!this.base.playlists) return;

        try {
            this.#playlists = (await this.base.playlists.asList()).map((r) =>
                brand(r.uri),
            );
        } catch (e: unknown) {
            console.error("Failed to get playlists");
            console.error(e);
        }
    }

    // Mixer

    #mute = $state(false);
    get mute() {
        return this.#mute;
    }
    set mute(mute: boolean) {
        void this.base.mixer?.setMute({ mute });
    }
    async #updateMute() {
        if (!this.base.mixer) return;

        try {
            this.#mute = (await this.base.mixer.getMute()) ?? false;
        } catch (e: unknown) {
            console.error("Failed to get mute");
            console.error(e);
        }
    }

    #volume = $state(100);
    get volume() {
        return this.#volume;
    }
    set volume(volume: number) {
        void this.base.mixer?.setVolume({ volume });
    }
    async #updateVolume() {
        if (!this.base.mixer) return;

        try {
            this.#volume = (await this.base.mixer.getVolume()) ?? 100;
        } catch (e: unknown) {
            console.error("Failed to get volume");
            console.error(e);
        }
    }

    // History

    #history = $state<[Date, string][]>([]);
    get history() {
        return this.#history;
    }
    async #updateHistory() {
        if (!this.base.history) return;

        try {
            this.#history = Object.entries(
                await this.base.history.getHistory(),
            ).flatMap(([date, tracks]) => {
                const d = new Date(parseInt(date, 10));
                return tracks.map((track) => [d, track.uri] as [Date, string]);
            });
        } catch (e: unknown) {
            console.error("Failed to get history");
            console.error(e);
        }
    }

    // Palette

    #palettes = new SvelteMap<string, string>();

    getPallete(url: string) {
        return this.#palettes.get(url);
    }

    #currentTrackPalette: string | null = $derived(
        this.#currentTrackImage
            ? (this.getPallete(this.#currentTrackImage) ?? null)
            : null,
    );
    get currentTrackPalette() {
        return this.#currentTrackPalette;
    }

    async requestPalette(url: string) {
        if (this.#palettes.has(url)) return this.#palettes.get(url);

        const img = new Image();
        img.crossOrigin = "";
        img.src = url;

        try {
            const theme = await themeFromImage(img);

            this.#palettes.set(
                url,
                Object.entries(theme.palettes)
                    .flatMap(([k, p]) =>
                        [
                            0, 4, 5, 6, 10, 12, 15, 17, 20, 22, 25, 30, 35, 40,
                            50, 60, 70, 80, 90, 92, 94, 95, 96, 98, 99, 100,
                        ].map(
                            (v) =>
                                `--color-${k.replace("V", "-v")}-${v.toString()}: #${(p.tone(v) & 0xffffff).toString(16).padStart(6, "0")}`,
                        ),
                    )
                    .join(";"),
            );

            return this.#palettes.get(url);
        } catch (e: unknown) {
            console.error("Failed to get palette");
            console.error(e);
        }
    }

    // Lyrics

    #lyrics = new SvelteMap<TrackURI, TrackLyrics>();

    getLyrics(uri: TrackURI) {
        return this.#lyrics.get(uri);
    }

    #currentTrackLyrics: TrackLyrics | null = $derived(
        this.#currentTrack
            ? (this.getLyrics(this.#currentTrack.track.uri) ?? null)
            : null,
    );
    get currentTrackLyrics() {
        return this.#currentTrackLyrics;
    }

    async requestLyrics(track: Track) {
        const uri = track.uri;

        if (this.#lyrics.has(uri)) return this.#lyrics.get(uri);

        try {
            const response = await lrclib.get({
                trackName: track.name,
                artistName: track.artists.map((a) => a.name).join(", "),
                albumName: track.album?.name,
                duration: Math.round(track.length / 1000),
            });

            if (!response.syncedLyrics) {
                this.#lyrics.set(uri, []);
                return [];
            }

            const pattern = /\[(\d+):(\d+).(\d+)\]\s*(.*)/;

            const lyrics = response.syncedLyrics.split("\n").flatMap((line) => {
                const match = line.match(pattern);

                if (match) {
                    const [, m, s, cs, lyrics] = match;

                    return [
                        {
                            timestamp:
                                10 *
                                (parseInt(cs) +
                                    100 * (parseInt(s) + 60 * parseInt(m))),
                            lyrics,
                        },
                    ];
                }

                return [];
            });

            this.#lyrics.set(uri, lyrics);
            return lyrics;
        } catch (e: unknown) {
            console.error("Failed to get lyrics");
            console.error(e);
        }
    }

    constructor() {
        this.base = new Mopidy({
            webSocketUrl: new URL("/mopidy/ws", WS_URL).toString(),
        });
    }

    init() {
        // Tracklist
        this.base.on("event:tracklistChanged", () => {
            void this.#updateQueue();
        });
        this.base.on("event:optionsChanged", () => {
            void this.#updateConsume();
            void this.#updateShuffle();
            void this.#updateRepeat();
            void this.#updateSingle();
        });

        // Playback
        this.base.on("event:seeked", ({ time_position }) => {
            this.#timePosition = time_position;
        });
        this.base.on("event:trackPlaybackStarted", ({ tl_track }) => {
            void this.#setCurrentTrack(tl_track as TlTrack);
            this.#timePosition = 0;
        });
        this.base.on("event:trackPlaybackEnded", () => {
            this.#currentTrack = null;
            this.#timePosition = null;
        });
        this.base.on("event:playbackStateChanged", ({ new_state }) => {
            this.#playbackState = new_state;
        });

        setInterval(() => {
            if (this.playbackState !== "playing") return;

            void this.#updateTimePosition();
        }, 100);

        // Library

        // Playlists

        // Mixer
        this.base.on("event:muteChanged", ({ mute }) => {
            this.#mute = mute;
        });
        this.base.on("event:volumeChanged", ({ volume }) => {
            this.#volume = volume;
        });

        // History

        // Palette

        // Lyrics

        return new Promise<void>((resolve, reject) => {
            this.base.on("state:online", () => {
                Promise.allSettled([
                    // Tracklist
                    this.#updateQueue(),
                    this.#updateConsume(),
                    this.#updateShuffle(),
                    this.#updateRepeat(),
                    this.#updateSingle(),

                    // Playback
                    this.#updateCurrentTrack(),
                    this.#updateTimePosition(),
                    this.#updatePlaybackState(),

                    // Library

                    // Playlists
                    this.#updatePlaylists(),

                    // Mixer
                    this.#updateMute(),
                    this.#updateVolume(),

                    // History
                    this.#updateHistory(),
                ])
                    .then(() => {
                        resolve();
                    })
                    .catch((e: unknown) => {
                        console.error("Failed to initialize Mopidy");
                        console.error(e);
                        reject(
                            new Error("Failed to initialize Mopidy", {
                                cause: e,
                            }),
                        );
                    });
            });
        });
    }
}

export default MopidyState;
