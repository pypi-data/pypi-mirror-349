<script lang="ts">
    import { formatDuration } from "$lib/format";
    import type MopidyState from "$lib/state/mopidy.svelte";
    import type { TlTrack, Track } from "$lib/types/mopidy";
    import { getContext } from "svelte";
    import { Virtualizer } from "virtua/svelte";
    import {
        Icon,
        List,
        ListItem,
        Menu,
        MenuItem,
        MenuList,
        MenuTrigger,
    } from "svelte-m3c";
    import { base } from "$app/paths";

    let { tracks }: { tracks: Track[] | TlTrack[] } = $props();

    let scroll = getContext("scroll") as () => HTMLElement | null;
    let scrollRef = $derived(scroll());

    let listRef = $state<HTMLElement | null>(null);

    let startMargin = $derived(
        listRef && scrollRef
            ? listRef.getBoundingClientRect().top -
                  scrollRef.getBoundingClientRect().top
            : 0,
    );

    let mopidy = getContext("mopidy") as MopidyState;

    $effect(() => {
        mopidy.requestImages(
            tracks.map((t) => ("track" in t ? t.track : t).uri),
        );
    });
</script>

<List bind:ref={listRef}>
    {#if scrollRef}
        <Virtualizer
            data={tracks}
            getKey={(item) => ("tlid" in item ? item.tlid : item.uri)}
            overscan={10}
            {scrollRef}
            {startMargin}
        >
            {#snippet children(item)}
                {@const track = "track" in item ? item.track : item}
                {@const active =
                    "tlid" in item
                        ? item.tlid === mopidy.currentTrack?.tlid
                        : item.uri === mopidy.currentTrack?.track.uri}

                <Menu type="context">
                    <MenuTrigger>
                        {#snippet child({ props })}
                            <ListItem
                                lines={2}
                                labelTextClass={active && "text-primary"}
                                supportingTextClass={active && "text-secondary"}
                                trailingClass={active && "text-secondary"}
                                {...props}
                            >
                                {#snippet leading()}
                                    {@const image = mopidy.getImage(track.uri)}

                                    {#if image}
                                        <img
                                            src={image}
                                            alt="Album cover"
                                            class="aspect-square h-full object-cover"
                                        />
                                    {/if}
                                {/snippet}
                                {#snippet labelText()}
                                    <a
                                        class="relative after:absolute after:inset-0 after:z-10 hover:underline"
                                        href="{base}/track/{encodeURIComponent(
                                            track.uri,
                                        )}"
                                    >
                                        {track.name}
                                    </a>
                                {/snippet}
                                {#snippet supportingText()}
                                    {#each track.artists as artist, index (artist.uri)}
                                        {#if index > 0},
                                        {/if}
                                        <a
                                            class="relative after:absolute after:inset-0 after:z-10 hover:underline"
                                            href="{base}/artist/{encodeURIComponent(
                                                artist.uri,
                                            )}"
                                        >
                                            {artist.name}
                                        </a>
                                    {/each}
                                    ‧
                                    <a
                                        class="relative after:absolute after:inset-0 after:z-10 hover:underline"
                                        href="{base}/album/{encodeURIComponent(
                                            track.album.uri,
                                        )}"
                                    >
                                        {track.album.name}
                                    </a>
                                {/snippet}
                                {#snippet trailing()}
                                    {formatDuration(track.length)}
                                {/snippet}
                            </ListItem>
                        {/snippet}
                    </MenuTrigger>

                    <MenuList>
                        <MenuItem>
                            {#snippet leading()}<Icon
                                    icon="play_arrow"
                                />{/snippet}
                            {#snippet text()}Play{/snippet}
                        </MenuItem>
                        <MenuItem>
                            {#snippet leading()}<Icon icon="resume" />{/snippet}
                            {#snippet text()}Play next{/snippet}
                        </MenuItem>
                        <MenuItem>
                            {#snippet leading()}<Icon icon="add" />{/snippet}
                            {#snippet text()}Add to queue{/snippet}
                        </MenuItem>
                    </MenuList>
                </Menu>
            {/snippet}
        </Virtualizer>
    {/if}
</List>
