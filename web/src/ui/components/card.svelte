<script lang="ts">
  import type { Size } from '../types';

  export let size: Size | undefined = undefined;

  const getSizeClasses = () => {
    switch (size) {
      case 'xs':
        return 'max-w-64';
      case 'sm':
        return 'max-w-96';
      case 'md':
        return 'max-w-screen-sm';
      case 'lg':
        return 'max-w-screen-md';
      case 'xl':
        return 'max-w-screen-lg';
      default:
        return '';
    }
  };

  const className = [getSizeClasses()].join(' ');
</script>

<div class="{className} flex max-w-s flex-col justify-between rounded-3xl bg-immich-gray p-5 dark:bg-immich-dark-gray">
  <slot />
</div>
