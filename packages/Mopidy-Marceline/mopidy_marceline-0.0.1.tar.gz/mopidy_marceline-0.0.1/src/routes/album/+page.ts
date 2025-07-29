import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
    const { mopidy } = await parent();

    const albumRefs = await mopidy.base.library?.browse({
        uri: "local:directory?type=album",
    });

    if (!albumRefs) {
        error(404, "No albums found");
    }

    console.debug("Album refs", albumRefs);

    const tracks = await mopidy.base.library?.lookup({
        uris: albumRefs
            .filter((albumRef) => albumRef.type === "album")
            .map((albumRef) => albumRef.uri),
    });

    if (!tracks) {
        error(404, "No albums found");
    }

    const albums = Object.values(tracks)
        .map((tracks) => tracks.at(0)?.album)
        .filter((album) => album !== undefined);

    await mopidy.requestImages(albums.map((album) => album.uri));

    return {
        albums,
    };
};
