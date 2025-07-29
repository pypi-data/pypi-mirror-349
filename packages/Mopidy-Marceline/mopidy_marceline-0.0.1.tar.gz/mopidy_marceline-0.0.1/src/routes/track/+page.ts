import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
    const { mopidy } = await parent();

    const trackRefs = await mopidy.base.library?.browse({
        uri: "local:directory?type=track",
    });

    if (!trackRefs) {
        error(404, "No tracks found");
    }

    const tracksObj = await mopidy.base.library?.lookup({
        uris: trackRefs
            .filter((trackRef) => trackRef.type === "track")
            .map((trackRef) => trackRef.uri),
    });

    if (!tracksObj) {
        error(404, "No albums found");
    }

    const tracks = Object.values(tracksObj).flatMap((tracks) => tracks);

    await mopidy.requestImages(tracks.map((track) => track.uri));

    return {
        tracks,
    };
};
