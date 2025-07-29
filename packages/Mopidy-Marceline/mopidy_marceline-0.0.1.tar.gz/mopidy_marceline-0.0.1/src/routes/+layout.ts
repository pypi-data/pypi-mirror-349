import MopidyState from "$lib/state/mopidy.svelte";
import type { LayoutLoad } from "./$types";

export const ssr = false;

export const load: LayoutLoad = async () => {
    const mopidy = new MopidyState();

    await mopidy.init();

    return {
        mopidy,
    };
};
