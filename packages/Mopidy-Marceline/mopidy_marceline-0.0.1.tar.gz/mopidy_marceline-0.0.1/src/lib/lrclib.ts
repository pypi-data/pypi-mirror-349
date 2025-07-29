import type { LRCLibResponse } from "./types/lrclib";

export const get = async (args: {
    trackName: string;
    artistName: string;
    albumName?: string;
    duration?: number;
}) => {
    const params = new URLSearchParams({
        track_name: args.trackName,
        artist_name: args.artistName,
        album_name: args.albumName ?? "",
        duration: args.duration?.toString() || "",
    });

    const response = await fetch(`https://lrclib.net/api/get?${params}`);

    if (!response.ok) throw new Error("Failed to fetch lyrics");

    return (await response.json()) as LRCLibResponse;
};
