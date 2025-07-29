import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
    const { mopidy } = await parent();

    await mopidy.requestImages(mopidy.queue.map((t) => t.track.uri));

    return {};
};
