<script lang="ts">
    import TrackList from "$lib/components/TrackList.svelte";
    import type MopidyState from "$lib/state/mopidy.svelte";
    import { getContext } from "svelte";

    import QueueActions from "$lib/components/QueueActions.svelte";

    let mopidy = getContext("mopidy") as MopidyState;
</script>

<svelte:head>
    <title>Queue</title>
</svelte:head>

<div class="flex flex-row items-center gap-2 px-4 pt-5 pb-2">
    <h1 class="shrink-0 grow text-display-l">Queue</h1>

    <QueueActions />
</div>

<TrackList tracks={mopidy.queue} />

<!-- <Lyrics /> -->
