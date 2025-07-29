import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
    const { mopidy } = await parent();

    const artistRefs = await mopidy.base.library?.browse({
        uri: "local:directory?type=artist&role=albumartist",
    });

    if (!artistRefs) {
        error(404, "No artists found");
    }

    console.debug("Artist refs", artistRefs);
    console.debug(
        await mopidy.base.library?.lookup({
            uris: ["local:artist:md5:4b00279b540280e05447024ad18e971d"],
        }),
    );

    console.debug(
        await mopidy.requestImages(
            artistRefs.map((artistRef) => artistRef.uri),
        ),
    );
    console.debug(
        await mopidy.requestImages([
            "local:artist:md5:4b00279b540280e05447024ad18e971d",
        ]),
    );

    return {};
};
