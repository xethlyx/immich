<script lang="ts">
  import { Colorspace, ImageFormat, type SystemConfigDto } from '@immich/sdk';
  import { isEqual } from 'lodash-es';
  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';
  import type { SettingsEventType } from '../admin-settings';
  import SettingSelect from '$lib/components/shared-components/settings/setting-select.svelte';

  import SettingSwitch from '$lib/components/shared-components/settings/setting-switch.svelte';
  import SettingButtonsRow from '$lib/components/shared-components/settings/setting-buttons-row.svelte';
  import SettingInputField, {
    SettingInputFieldType,
  } from '$lib/components/shared-components/settings/setting-input-field.svelte';

  export let savedConfig: SystemConfigDto;
  export let defaultConfig: SystemConfigDto;
  export let config: SystemConfigDto; // this is the config that is being edited
  export let disabled = false;

  const dispatch = createEventDispatcher<SettingsEventType>();
</script>

<div>
  <div in:fade={{ duration: 500 }}>
    <form autocomplete="off" on:submit|preventDefault>
      <div class="ml-4 mt-4 flex flex-col gap-4">
        <SettingSelect
          label="THUMBNAIL FORMAT"
          desc="Format used for generated thumbnail images. WebP produces smaller files at the same quality."
          number
          bind:value={config.thumbnail.thumbnailFormat}
          options={[
            { value: ImageFormat.Jpeg, text: 'JPEG' },
            { value: ImageFormat.Webp, text: 'WEBP' },
          ]}
          name="resolution"
          isEdited={config.thumbnail.thumbnailFormat !== savedConfig.thumbnail.thumbnailFormat}
          {disabled}
        />

        <SettingSelect
          label="THUMBNAIL RESOLUTION"
          desc="Used when viewing groups of photos (main timeline, album view, etc.). Higher resolutions can preserve more detail but take longer to encode, have larger file sizes, and can reduce app responsiveness."
          number
          bind:value={config.thumbnail.thumbnailSize}
          options={[
            { value: 1080, text: '1080p' },
            { value: 720, text: '720p' },
            { value: 480, text: '480p' },
            { value: 250, text: '250p' },
            { value: 200, text: '200p' },
          ]}
          name="resolution"
          isEdited={config.thumbnail.thumbnailSize !== savedConfig.thumbnail.thumbnailSize}
          {disabled}
        />

        <SettingSelect
          label="PREVIEW FORMAT"
          desc="Format used for generated preview images. WebP produces smaller files at the same quality."
          number
          bind:value={config.thumbnail.thumbnailFormat}
          options={[
            { value: ImageFormat.Jpeg, text: 'JPEG' },
            { value: ImageFormat.Webp, text: 'WEBP' },
          ]}
          name="resolution"
          isEdited={config.thumbnail.thumbnailFormat !== savedConfig.thumbnail.thumbnailFormat}
          {disabled}
        />

        <SettingSelect
          label="PREVIEW RESOLUTION"
          desc="Used when viewing a single photo and for machine learning. Higher resolutions can preserve more detail but take longer to encode, have larger file sizes, and can reduce app responsiveness."
          number
          bind:value={config.thumbnail.previewSize}
          options={[
            { value: 2160, text: '4K' },
            { value: 1440, text: '1440p' },
            { value: 1080, text: '1080p' },
            { value: 720, text: '720p' },
          ]}
          name="resolution"
          isEdited={config.thumbnail.previewSize !== savedConfig.thumbnail.previewSize}
          {disabled}
        />

        <SettingInputField
          inputType={SettingInputFieldType.NUMBER}
          label="QUALITY"
          desc="Image quality from 1-100. Higher is better for quality but produces larger files."
          bind:value={config.thumbnail.quality}
          isEdited={config.thumbnail.quality !== savedConfig.thumbnail.quality}
        />

        <SettingSwitch
          title="PREFER WIDE GAMUT"
          subtitle="Use Display P3 for thumbnails. This better preserves the vibrance of images with wide colorspaces, but images may appear differently on old devices with an old browser version. sRGB images are kept as sRGB to avoid color shifts."
          checked={config.thumbnail.colorspace === Colorspace.P3}
          on:toggle={(e) => (config.thumbnail.colorspace = e.detail ? Colorspace.P3 : Colorspace.Srgb)}
          isEdited={config.thumbnail.colorspace !== savedConfig.thumbnail.colorspace}
        />
      </div>

      <div class="ml-4">
        <SettingButtonsRow
          on:reset={({ detail }) => dispatch('reset', { ...detail, configKeys: ['thumbnail'] })}
          on:save={() => dispatch('save', { thumbnail: config.thumbnail })}
          showResetToDefault={!isEqual(savedConfig, defaultConfig)}
          {disabled}
        />
      </div>
    </form>
  </div>
</div>
