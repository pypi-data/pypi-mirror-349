<script lang="ts">
    import Title from "$lib/components/Title.svelte";
    import TrackList from "$lib/components/TrackList.svelte";
    import TrackListActions from "$lib/components/TrackListActions.svelte";

    let { data } = $props();
</script>

<svelte:head>
    <Title text="All tracks" />
</svelte:head>

<div class="flex flex-row items-center gap-2 px-4 pt-5 pb-2">
    <h1 class="shrink-0 grow text-display-l">All tracks</h1>

    <TrackListActions tracks={data.tracks} />
</div>

<TrackList tracks={data.tracks} />
