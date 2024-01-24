<script lang="ts">
  import { moonPath, moonViewBox, sunPath, sunViewBox } from '$lib/assets/svg-paths';
  import { Theme } from '$lib/constants';
  import { createEventDispatcher } from 'svelte';
  import IconButton from './icon-button.svelte';
  import Icon from './icon.svelte';

  export let theme: Theme = Theme.LIGHT;
  export let title = 'Toggle theme';

  const dispatch = createEventDispatcher<{ theme: Theme }>();
  const onClick = () => {
    theme = theme === Theme.LIGHT ? Theme.DARK : Theme.LIGHT;
    dispatch('theme', theme);
  };
</script>

<IconButton on:click={onClick} {title}>
  {#if theme === Theme.LIGHT}
    <Icon path={moonPath} viewBox={sunViewBox} class="h-6 w-6" />
  {:else}
    <Icon path={sunPath} viewBox={moonViewBox} class="h-6 w-6" />
  {/if}
</IconButton>
