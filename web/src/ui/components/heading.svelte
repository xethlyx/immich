<script lang="ts">
  import type { Size } from '../types';

  export let id: string | undefined = undefined;
  export let size: Size = 'xl';
  export let color: 'primary' = 'primary';

  const getColorClasses = () => {
    switch (color) {
      case 'primary':
        return 'text-immich-primary dark:text-immich-dark-primary';
    }
  };

  const getSizeClasses = () => {
    switch (size) {
      case 'xl':
        return 'text-4xl';
      case 'lg':
        return 'text-2xl';
      case 'md':
        return 'text-xl';
      case 'sm':
        return 'text-lg';
      case 'xs':
        return 'text-md';
    }
  };

  const className = [getColorClasses(), getSizeClasses()].join(' ');
</script>

{#if size === 'xl'}
  <h1 {id} class={className}><slot /></h1>
{:else if size === 'lg'}
  <h2 {id} class={className}><slot /></h2>
{:else if size === 'md'}
  <h3 {id} class={className}><slot /></h3>
{:else if size === 'sm'}
  <h4 {id} class={className}><slot /></h4>
{:else if size === 'xs'}
  <h5 {id} class={className}><slot /></h5>
{/if}
