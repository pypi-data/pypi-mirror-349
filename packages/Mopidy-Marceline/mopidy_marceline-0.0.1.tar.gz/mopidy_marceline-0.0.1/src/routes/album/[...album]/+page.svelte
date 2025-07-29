<script lang="ts">
    import Title from "$lib/components/Title.svelte";
    import TrackList from "$lib/components/TrackList.svelte";
    import TrackListActions from "$lib/components/TrackListActions.svelte";
    import type MopidyState from "$lib/state/mopidy.svelte.js";
    import { getContext } from "svelte";

    let { data } = $props();

    let mopidy = getContext("mopidy") as MopidyState;

    let image = $derived(mopidy.getImage(data.album.uri));
</script>

<svelte:head>
    <Title text={data.album.name} />
</svelte:head>

<div class="mx-auto flex h-full max-w-(--breakpoint-large) flex-col">
    <div class="flex flex-col items-center gap-8 p-4 pt-8 medium:flex-row">
        <img src={image} class="h-auto w-full max-w-100" />
        <div class="flex flex-col">
            <h1 class="text-display-l">{data.album.name}</h1>
            <span class="mb-4 text-display-s text-on-surface-variant"
                >{data.album.artists
                    .map((artist) => artist.name)
                    .join(", ")}</span
            >

            <TrackListActions tracks={data.tracks} />
        </div>
    </div>

    {#if data.tracks.length > 0}
        <TrackList tracks={data.tracks} />
    {:else}
        <p class="text-title-m text-on-surface-variant">No tracks available</p>
    {/if}
</div>
