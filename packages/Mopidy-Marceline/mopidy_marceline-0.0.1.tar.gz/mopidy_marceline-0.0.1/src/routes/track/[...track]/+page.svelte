<script lang="ts">
    import Title from "$lib/components/Title.svelte";
    import { SEPARATOR } from "$lib/constants.js";
    import type MopidyState from "$lib/state/mopidy.svelte.js";
    import { getContext } from "svelte";

    let { data } = $props();

    let mopidy = getContext("mopidy") as MopidyState;

    let image = $derived(mopidy.getImage(data.track.uri));
</script>

<svelte:head>
    <Title text={data.track.name} />
</svelte:head>

<div
    class="mx-auto flex h-full max-w-(--breakpoint-large) flex-col items-center gap-8 p-8 medium:flex-row"
>
    <img src={image} class="h-auto w-full max-w-100" />
    <div>
        <h1 class="text-display-l">{data.track.name}</h1>
        <div class="flex flex-row gap-4 text-display-s text-on-surface-variant">
            <span
                >{data.track.artists
                    .map((artist) => artist.name)
                    .join(", ")}</span
            >
            <span>{SEPARATOR}</span>
            <a class="hover:underline" href="/album/{data.track.album.uri}"
                >{data.track.album.name}</a
            >
        </div>
    </div>
</div>
