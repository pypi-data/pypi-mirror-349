<script lang="ts">
    import type MopidyState from "$lib/state/mopidy.svelte";
    import { getContext } from "svelte";
    import {
        Button,
        IconButton,
        Menu,
        MenuList,
        MenuTrigger,
    } from "svelte-m3c";

    let mopidy = getContext("mopidy") as MopidyState;
</script>

<div class="flex flex-row items-center gap-2">
    <Button
        variant="filled"
        icon="clear"
        onclick={async () => {
            await mopidy.base.tracklist?.clear();
        }}
    >
        Clear
    </Button>

    <Button
        containerClass="max-medium:hidden"
        icon="shuffle"
        onclick={async () => {
            await mopidy.base.tracklist?.shuffle({});
        }}
    >
        Shuffle
    </Button>

    <Menu type="dropdown">
        <MenuTrigger>
            {#snippet child({ props })}
                <IconButton
                    containerClass="medium:hidden"
                    icon="more_horiz"
                    {...props}
                />
            {/snippet}
        </MenuTrigger>
        <MenuList></MenuList>
    </Menu>
</div>
