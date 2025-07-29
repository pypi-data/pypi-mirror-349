import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, parent }) => {
    const { mopidy } = await parent();

    const track = (
        await mopidy.base.library?.lookup({ uris: [params.track] })
    )?.[params.track].at(0);

    if (!track) {
        console.error("Track not found", params.track);
        error(404, "Track not found");
    }

    const image = (await mopidy.requestImages([track.uri]))?.at(0);
    const palette = image ? await mopidy.requestPalette(image) : undefined;

    return {
        track,
        palette,
    };
};
