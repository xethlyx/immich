import type { PageLoad } from './$types';

// export const ssr = false;
// export const csr = false;

export const load = (async () => {
  return {
    meta: {
      title: 'Design',
      description: 'Immich UI Design',
    },
  };
}) satisfies PageLoad;
