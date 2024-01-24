<script lang="ts">
  import Icon from './icon.svelte';
  import Button from './button.svelte';
  import type { Color } from '../types';

  export let icon = '';
  export let title = '';
  export let transparent = true;
  export let color: Color = 'primary';
</script>

<Button {title} {transparent} {color} size="icon" rounded="full" on:click>
  <slot>
    <Icon path={icon} />
  </slot>
</Button>
