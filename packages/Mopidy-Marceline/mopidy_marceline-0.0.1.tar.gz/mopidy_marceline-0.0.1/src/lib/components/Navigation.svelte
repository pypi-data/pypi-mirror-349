<script module lang="ts">
    import type { ComponentProps } from "svelte";
    import type { Icon } from "svelte-m3c";

    const destinations = [
        {
            label: "Queue",
            icon: "playlist_play",
            href: "/",
        },
        {
            label: "Library",
            icon: "folder",
            href: "/library",
        },
        {
            label: "Artists",
            icon: "artist",
            href: "/artist",
        },
        {
            label: "Albums",
            icon: "album",
            href: "/album",
        },
        {
            label: "Tracks",
            icon: "music_note",
            href: "/track",
        },
        {
            label: "Playlists",
            icon: "queue_music",
            href: "/playlist",
        },
        {
            label: "History",
            icon: "history",
            href: "/history",
        },
    ] as const satisfies {
        label: string;
        icon: ComponentProps<typeof Icon>["icon"];
        href: string;
    }[];
</script>

<script lang="ts">
    import { base } from "$app/paths";
    import { page } from "$app/state";
    import {
        NavigationDrawer,
        NavigationDrawerItem,
        NavigationRail,
        NavigationRailItem,
    } from "svelte-m3c";

    let active = $derived(
        destinations.findLastIndex(({ href }) =>
            page.url.pathname.includes(href),
        ),
    );
</script>

<NavigationDrawer class="max-large:hidden">
    {#each destinations as { label, icon, href }, index (index)}
        <NavigationDrawerItem
            {icon}
            href="{base}{href}"
            active={index === active}
        >
            {label}
        </NavigationDrawerItem>
    {/each}
</NavigationDrawer>

<NavigationRail class="py-8 max-medium:hidden large:hidden">
    {#each destinations as { label, icon, href }, index (index)}
        <NavigationRailItem
            {icon}
            href="{base}{href}"
            active={index === active}
        >
            {label}
        </NavigationRailItem>
    {/each}
</NavigationRail>
