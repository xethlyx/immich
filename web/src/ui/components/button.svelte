<script lang="ts">
  import type { Color } from '../types';

  export let type: HTMLButtonElement['type'] = 'button';
  export let disabled = false;
  export let title = '';
  export let rounded: 'semi' | 'full' | boolean = true;
  export let color: Color = 'primary';
  export let transparent = false;
  export let size: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'size' | 'icon' = 'md';
  export let fullWidth = false;

  const getBaseClasses = () => {
    return 'inline-flex items-center justify-center transition-colors disabled:cursor-not-allowed disabled:opacity-60';
  };

  const getHoverClasses = () => {
    if (transparent) {
      return 'enabled:hover:bg-gray-100 enabled:dark:hover:bg-gray-700';
    }

    switch (color) {
      case 'primary':
        return 'enabled:dark:hover:bg-immich-dark-primary/80 enabled:hover:bg-immich-primary/90';

      case 'secondary':
        return 'enabled:dark:hover:bg-gray-200/90 enabled:hover:bg-gray-500/90 ';

      case 'info':
        return 'enabled:hover:bg-blue-300/90';

      case 'success':
        return 'enabled:hover:bg-green-300/90';

      case 'warning':
        return 'enabled:hover:bg-yellow-300/90';

      case 'danger':
        return 'enabled:hover:bg-red-300/90';
    }
  };

  const getBackgroundClasses = () => {
    switch (color) {
      case 'primary':
        return 'bg-immich-primary dark:bg-immich-dark-primary';

      case 'secondary':
        return 'bg-gray-500 dark:bg-gray-200';

      case 'info':
        return 'bg-blue-500';

      case 'success':
        return 'bg-green-500';

      case 'warning':
        return 'bg-yellow-500';

      case 'danger':
        return 'bg-red-500';
    }
  };

  const getColorClasses = () => {
    switch (color) {
      case 'primary':
        return transparent ? 'text-gray-500 dark:text-immich-dark-primary' : 'text-white dark:text-immich-dark-gray';

      case 'secondary':
        return transparent ? 'text-gray-500 dark:text-immich-dark-gray' : 'text-white dark:text-immich-dark-gray';

      case 'info':
        return transparent ? 'text-blue-500' : 'text-gray-800';

      case 'success':
        return transparent ? 'text-green-500' : 'text-gray-800';

      case 'warning':
        return transparent ? 'text-yellow-500' : 'text-gray-800';

      case 'danger':
        return transparent ? 'text-red-500' : 'text-white';
    }
  };

  const getSizeClasses = () => {
    switch (size) {
      case 'xs':
        return 'p-2 text-xs';
      case 'sm':
        return 'px-4 py-2 text-sm';
      case 'icon':
        return 'p-2.5';
      case 'md':
        return 'px-4 py-2 text-base';
      case 'lg':
        return 'px-6 py-3 text-lg';
      case 'xl':
        return 'px-8 py-4 text-2xl';
    }
  };

  const getWidthClasses = () => {
    return fullWidth ? 'w-full' : '';
  };

  const getRoundedClasses = () => {
    switch (rounded) {
      case 'full':
        return 'rounded-full';

      case true:
      case 'semi':
        return 'rounded-lg';

      case false:
      default:
        return 'rounded-sm';
    }
  };

  const className = [
    transparent ? '' : getBackgroundClasses(),
    getHoverClasses(),
    getBaseClasses(),
    getWidthClasses(),
    getRoundedClasses(),
    getColorClasses(),
    getSizeClasses(),
  ].join(' ');
</script>

<div class={getWidthClasses()}>
  <button on:click {type} {disabled} {title} class={className}>
    <slot />
  </button>
</div>
