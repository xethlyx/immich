<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import Icon from './icon.svelte';

  export let title: string;
  export let icon: string;
  export let isSelected = false;
  export let iconFlipped = false;

  const dispatch = createEventDispatcher<{ click: void }>();
  const onClick = () => dispatch('click');

  const selectedClasses = isSelected
    ? 'bg-immich-primary/10 text-immich-primary hover:bg-immich-primary/25 dark:bg-immich-dark-primary/10 dark:text-immich-dark-primary'
    : '';
</script>

<button
  on:click={onClick}
  on:keydown={onClick}
  class="{selectedClasses} flex w-full place-items-center justify-between gap-4 rounded-r-full py-3 transition-[padding] delay-100 duration-100 hover:cursor-pointer hover:bg-immich-gray hover:text-immich-primary dark:text-immich-dark-fg dark:hover:bg-immich-dark-gray dark:hover:text-immich-dark-primary pl-5 group-hover:sm:px-5 md:px-5"
>
  <div class="flex w-full place-items-center gap-4 overflow-hidden truncate">
    <Icon path={icon} size="1.5em" class="shrink-0" flipped={iconFlipped} />
    <p class="text-sm font-medium">{title}</p>
  </div>

  <div
    class="h-0 overflow-hidden transition-[height] delay-1000 duration-100 sm:group-hover:h-auto group-hover:sm:overflow-visible md:h-auto md:overflow-visible"
  ></div>
</button>
