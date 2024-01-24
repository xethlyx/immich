<script lang="ts">
  import Heading from './heading.svelte';

  export let title = '';

  const titleClass = title ? 'top-16 h-[calc(100%-theme(spacing.16))]' : 'top-0 h-full';
  const hasHeader = !!$$slots.header;
  const headerPadding = hasHeader ? 'pt-[var(--navbar-height)]' : '';
</script>

{#if hasHeader}
  <header class="fixed z-[900] h-[var(--navbar-height)] w-screen">
    <slot name="header" />
  </header>
{/if}
<main
  class="relative grid h-screen grid-cols-[theme(spacing.18)_auto] overflow-hidden bg-immich-bg {headerPadding} dark:bg-immich-dark-bg md:grid-cols-[theme(spacing.64)_auto]"
>
  <slot name="sidebar" />

  <section class="relative h-full">
    {#if title}
      <div
        class="absolute flex h-16 w-full place-items-center justify-between border-b p-4 dark:border-immich-dark-gray dark:text-immich-dark-fg"
      >
        <Heading size="lg">{title}</Heading>
        <slot name="buttons" />
      </div>
    {/if}

    <div id="content" class="immich-scrollbar p-4 pb-8 scrollbar-stable absolute {titleClass} w-full overflow-y-auto">
      <slot />
    </div>
  </section>
</main>
