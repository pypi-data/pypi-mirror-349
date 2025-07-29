import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, parent }) => {
    const { mopidy } = await parent();

    const uri = params.album;

    const lookup = await mopidy.base.library?.lookup({ uris: [uri] });
    const tracks = lookup?.[uri];
    const album = tracks?.at(0)?.album;

    if (!album || !tracks) {
        console.error("Album not found", uri);
        error(404, "Album not found");
    }

    const image = (await mopidy.requestImages([album.uri]))?.at(0);
    const palette = image ? await mopidy.requestPalette(image) : undefined;

    return {
        album,
        tracks,
        palette,
    };
};
