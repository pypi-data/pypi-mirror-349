<script lang="ts">
    import Player from "$lib/components/Player.svelte";
    import { Provider, ScrollArea } from "svelte-m3c";
    import "../app.css";
    import { page } from "$app/state";
    import { setContext } from "svelte";
    import Navigation from "$lib/components/Navigation.svelte";
    import Search from "$lib/components/Search.svelte";

    let { children, data } = $props();

    let scrollRef = $state(null);
    setContext("scroll", () => scrollRef);

    let mopidy = $state(data.mopidy);
    setContext("mopidy", mopidy);

    let palette = $derived(
        page.data.palette ?? mopidy.currentTrackPalette ?? "",
    );
</script>

<Provider>
    <div
        class="flex h-full flex-col bg-surface text-on-surface palette"
        style={palette}
    >
        <div class="flex h-full flex-row pb-20">
            <Navigation />
            <ScrollArea bind:viewportRef={scrollRef}>
                <Search />
                <main class="min-h-full">
                    {@render children()}
                </main>
            </ScrollArea>
        </div>
        <Player />
    </div>
</Provider>
