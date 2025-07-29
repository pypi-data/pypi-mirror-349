<script lang="ts">
    import Title from "$lib/components/Title.svelte";
    import type MopidyState from "$lib/state/mopidy.svelte";
    import { getContext } from "svelte";

    let { data } = $props();

    let mopidy = getContext("mopidy") as MopidyState;
</script>

<svelte:head>
    <Title text="All albums" />
</svelte:head>

<div class="grid grid-cols-4 gap-4">
    {#each data.albums as album (album.uri)}
        <img src={mopidy.getImage(album.uri)} />
    {/each}
</div>
