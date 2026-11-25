// news-image-20261124 — "THE WORLD IN ONE DAY" (Tuesday 24 November 2026).
//
// The entry is the newspaper front page in entry.png beside this file; the
// program copies it to the output directory. Node 22, standard library only,
// no network, no stdin. Outside the grader, MAKEFUN_OUTPUT_DIR stands in
// for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'),
);
