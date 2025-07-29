import adapter from "@sveltejs/adapter-static";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: vitePreprocess(),

    kit: {
        adapter: adapter({
            assets: "mopidy_marceline/static",
            fallback: "index.html",
            pages: "mopidy_marceline/static",
        }),
        paths: {
            base: process.env.NODE_ENV === "production" ? "/marceline" : "",
        },
    },
};

export default config;
