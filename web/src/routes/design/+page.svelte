<script lang="ts">
  import {
    mdiBookMultiple,
    mdiButtonCursor,
    mdiCardMultipleOutline,
    mdiFormatHeader1,
    mdiHeartMultiple,
    mdiImageMultiple,
    mdiPlus,
    mdiSquare,
    mdiTrashCan,
  } from '@mdi/js';
  import Button from '@ui/components/button.svelte';
  import Card from '@ui/components/card.svelte';
  import Heading from '@ui/components/heading.svelte';
  import IconButton from '@ui/components/icon-button.svelte';
  import Layout from '@ui/components/layout.svelte';
  import SidebarItem from '@ui/components/sidebar-item.svelte';
  import Sidebar from '@ui/components/sidebar.svelte';
  import ThemeSwitcher from '@ui/components/theme-switcher.svelte';
  import type { Color, Size } from '@ui/types';
  import { colorTheme } from '../../lib/stores/preferences.store';

  const sizes: Size[] = ['xs', 'sm', 'md', 'lg', 'xl'];
  const colors: Color[] = ['primary', 'secondary', 'info', 'success', 'warning', 'danger'];

  const scrollTo = (id: string) => {
    const content = document.getElementById('content');
    const anchor = document.getElementById(id);
    if (!anchor || !content) {
      return;
    }

    content.scrollTo({ top: anchor.offsetTop - 24, behavior: 'smooth' });
  };
</script>

<Layout>
  <!-- <AppBar slot="header" /> -->
  <div class="h-full" slot="sidebar">
    <Sidebar>
      <SidebarItem title="Headings" icon={mdiFormatHeader1} on:click={() => scrollTo('headings')}></SidebarItem>
      <SidebarItem title="Buttons" icon={mdiButtonCursor} on:click={() => scrollTo('buttons')}></SidebarItem>
      <SidebarItem title="Cards" icon={mdiCardMultipleOutline} on:click={() => scrollTo('cards')}></SidebarItem>
      <SidebarItem title="Sidebar" icon={mdiSquare} on:click={() => scrollTo('sidebar')}></SidebarItem>
    </Sidebar>
  </div>

  <main class="m-8 pb-16">
    <Heading size="xl">Design</Heading>

    <section class="py-4 flex flex-col gap-2">
      <Heading size="lg">Theme Switcher</Heading>
      <ThemeSwitcher on:theme={({ detail }) => ($colorTheme = { value: detail, system: false })}></ThemeSwitcher>
    </section>

    <section class="py-4 flex flex-col gap-2">
      <Heading id="headings" size="lg">Headings</Heading>
      {#each sizes as size}
        <Heading {size}>Heading ({size})</Heading>
      {/each}
    </section>

    <section class="py-4 flex flex-col gap-2">
      <Heading id="buttons" size="lg">Buttons</Heading>

      <Heading size="md">Colors</Heading>
      <div class="flex gap-2">
        <Button color="primary">Primary</Button>
        <Button color="secondary">Secondary</Button>
        <Button color="success">Success</Button>
        <Button color="info">Info</Button>
        <Button color="warning">Warning</Button>
        <Button color="danger">Danger</Button>
      </div>

      <Heading size="md">Disabled</Heading>
      <div class="flex gap-2">
        <Button disabled color="primary">Primary</Button>
        <Button disabled color="secondary">Secondary</Button>
        <Button disabled color="success">Success</Button>
        <Button disabled color="info">Info</Button>
        <Button disabled color="warning">Warning</Button>
        <Button disabled color="danger">Danger</Button>
      </div>

      <Heading size="md">Rounded</Heading>
      <div class="flex align-top gap-2">
        <Button rounded="full" color="secondary">Rounded</Button>
        <Button rounded="semi" color="warning">Semi Rounded</Button>
        <Button rounded={false} color="info">None</Button>
      </div>

      <Heading size="md">Sizes</Heading>
      <div class="flex gap-2">
        <Button size="xs">Extra Small</Button>
        <Button size="sm">Small</Button>
        <Button size="md">Medium</Button>
        <Button size="lg">Large</Button>
        <Button size="xl">Extra Large</Button>
      </div>

      <Heading size="md">Width</Heading>
      <div class="flex flex-col gap-2 max-w-[500px]">
        <Button fullWidth color="primary">Primary</Button>
        <Button fullWidth color="secondary">Secondary</Button>
        <Button fullWidth color="success">Success</Button>
        <Button fullWidth color="info">Info</Button>
        <Button fullWidth color="warning">Warning</Button>
        <Button fullWidth color="danger">Danger</Button>
      </div>

      <Heading size="md">Icon Buttons</Heading>
      <div class="flex gap-2 max-w-[500px]">
        {#each colors as color}
          <IconButton {color} icon={mdiPlus} />
        {/each}
      </div>
      <div class="flex gap-2 max-w-[500px]">
        {#each colors as color}
          <IconButton transparent={false} {color} icon={mdiPlus} />
        {/each}
      </div>

      <Heading size="md">Events</Heading>
      <div class="flex gap-2">
        <Button on:click={() => alert('Hello')}>on:click</Button>
      </div>
    </section>

    <section class="py-4 flex flex-col gap-2">
      <Heading id="cards" size="lg">Cards</Heading>

      <div class="flex flex-col gap-2">
        {#each sizes as size}
          <Card {size}>
            <Heading size="lg">Card ({size})</Heading>
            <p class="dark:text-immich-dark-fg text-immich-fg">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Soluta dignissimos cupiditate eum ut nesciunt
              architecto excepturi veritatis facere exercitationem? Quasi maiores modi voluptatum impedit vero, quae
              dolorum officia molestiae consequuntur.
            </p>
          </Card>
        {/each}
      </div>
    </section>

    <section class="py-4 flex flex-col gap-2">
      <Heading id="sidebar" size="lg">Sidebar</Heading>
      <Sidebar>
        <SidebarItem title="Item A" icon={mdiImageMultiple} isSelected></SidebarItem>
        <SidebarItem title="Item B" icon={mdiHeartMultiple}></SidebarItem>
        <SidebarItem title="Item C" icon={mdiBookMultiple}></SidebarItem>
        <SidebarItem title="Item D" icon={mdiTrashCan}></SidebarItem>
      </Sidebar>
    </section>

    <!-- <section class="py-4 flex flex-col gap-2">
    <Heading size="lg">Layouts</Heading>
  </section> -->

    <!-- <section class="py-4 flex flex-col gap-2">
    <Heading size="lg">Layouts</Heading>

    <div class="max-w-[750px] border border-white">
      <Layout>
        <div class="p-2" slot="header">
          <Heading size="lg">Header</Heading>
        </div>
        <div class="p-2 w-full border border-white" slot="sidebar">
          <Heading size="lg">Sidebar</Heading>
        </div>
        <div class="p-2 w-full border border-white h-[500px]">
          <Heading size="lg">Content</Heading>
        </div>
      </Layout>
    </div>

    <div class="max-w-[750px] border border-white">
      <Layout title="Content Title">
        <div class="p-2" slot="header">
          <Heading size="lg">Header</Heading>
        </div>
        <div class="p-2 w-full border border-white" slot="sidebar">
          <Heading size="lg">Sidebar</Heading>
        </div>
        <div class="p-2 w-full border border-white h-[500px]">
          <Heading size="md">Content</Heading>
        </div>
      </Layout>
    </div>
  </section> -->
  </main>
</Layout>
