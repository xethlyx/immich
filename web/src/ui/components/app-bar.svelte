<div class="absolute top-0 w-full z-[100] bg-transparent">
  <div
    class="grid grid-cols-[10%_80%_10%] justify-between md:grid-cols-[20%_60%_20%] lg:grid-cols-3 mx-2 mt-2 place-items-center rounded-lg p-2 transition-all dark:bg-immich-dark-gray bg-immich-dark-gray text-white"
  >
    <div class="flex place-items-center gap-6 justify-self-start dark:text-immich-dark-fg">
      <slot name="leading" />
    </div>

    <div class="w-full">
      <slot />
    </div>

    <div class="mr-4 flex place-items-center gap-1 justify-self-end">
      <slot name="trailing" />
    </div>
  </div>
</div>
