<script lang="ts">
    import type MopidyState from "$lib/state/mopidy.svelte";
    import type { Track, TrackURI } from "$lib/types/mopidy";
    import { getContext } from "svelte";
    import {
        Button,
        Icon,
        IconButton,
        Menu,
        MenuItem,
        MenuList,
        MenuTrigger,
    } from "svelte-m3c";

    let { tracks }: { tracks: Track[] | TrackURI[] } = $props();

    let opts = $derived(
        tracks.length > 0
            ? typeof tracks[0] === "string"
                ? {
                      uris: tracks as TrackURI[],
                  }
                : {
                      tracks: tracks as Track[],
                  }
            : {},
    );

    let mopidy = getContext("mopidy") as MopidyState;
</script>

<div class="flex flex-row items-center gap-2">
    <Button
        variant="filled"
        icon="play_arrow"
        onclick={async () => {
            await mopidy.base.tracklist?.clear();
            await mopidy.base.tracklist?.add(opts);
            await mopidy.base.playback?.play({});
        }}
    >
        Play
    </Button>

    <Menu type="dropdown">
        <MenuTrigger>
            {#snippet child({ props })}
                <IconButton icon="more_horiz" {...props} />
            {/snippet}
        </MenuTrigger>
        <MenuList>
            <MenuItem
                onSelect={() => {
                    mopidy.base.tracklist?.add({
                        ...opts,
                        at_position: 1,
                    });
                }}
            >
                {#snippet leading()}
                    <Icon icon="resume" />
                {/snippet}
                {#snippet text()}
                    Play next
                {/snippet}
            </MenuItem>
            <MenuItem
                onSelect={() => {
                    mopidy.base.tracklist?.add(opts);
                }}
            >
                {#snippet leading()}
                    <Icon icon="add" />
                {/snippet}
                {#snippet text()}
                    Add to queue
                {/snippet}
            </MenuItem>
        </MenuList>
    </Menu>
</div>
