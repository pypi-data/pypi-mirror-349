<script lang="ts">
    import type MopidyState from "$lib/state/mopidy.svelte";
    import { getContext } from "svelte";
    import { SvelteMap } from "svelte/reactivity";

    let mopidy = getContext("mopidy") as MopidyState;

    let autoScroll = $state(true);
    let elements = new SvelteMap<number, HTMLElement>();
    let container: HTMLElement | undefined = $state(undefined);

    let currentTimestamp = $derived.by(() => {
        if (!mopidy.timePosition || !mopidy.currentTrackLyrics) return null;

        const currentTime = mopidy.timePosition;

        return (
            mopidy.currentTrackLyrics.findLast(
                ({ timestamp }) => currentTime >= timestamp,
            )?.timestamp ?? null
        );
    });

    $effect(() => {
        if (autoScroll)
            if (currentTimestamp)
                elements.get(currentTimestamp)?.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "nearest",
                });
            else
                container?.scrollTo({
                    top: 0,
                    behavior: "smooth",
                });
    });
</script>

{#if mopidy.currentTrackLyrics}
    <div
        class="relative flex h-full flex-col gap-1 overflow-y-auto scroll-smooth text-center text-display-s text-on-surface-variant"
        bind:this={container}
    >
        <div class="h-[50dvh]"></div>
        {#each mopidy.currentTrackLyrics as lyric (lyric.timestamp)}
            {@const isCurrent = currentTimestamp === lyric.timestamp}
            {@const get = () => elements.get(lyric.timestamp)!}
            {@const set = (el: HTMLElement) =>
                el
                    ? elements.set(lyric.timestamp, el)
                    : elements.delete(lyric.timestamp)}

            <p
                class={[
                    "transition-all",
                    isCurrent && "my-3 text-display-m text-tertiary",
                ]}
                bind:this={get, set}
            >
                {lyric.lyrics}
            </p>
        {/each}
        <div class="h-[50dvh]"></div>
    </div>
{/if}
