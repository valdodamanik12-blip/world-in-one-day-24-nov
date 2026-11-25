# THE WORLD IN ONE DAY — Tuesday 24 November 2026

[![make.fun — news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/valdodamanik12-blip/world-in-one-day-24-nov/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/valdodamanik12-blip/world-in-one-day-24-nov/reward.svg)](https://make.fun/bounty/news-image-20261124)

A newspaper front page that sums up the world's news of Tuesday 24 November 2026 in one
image — six stories, from Riyadh to Villavicencio, drawn by `render.py` and shipped as
`entry.png`.

**The six stories:** the Houthis hit Riyadh's PIF Tower for the second time in a week
(11 wounded); a Russian strike on a Zaporizhzhia apartment block (2 dead, 40 wounded); Israel
kills Hamas internal security chief Naeem Abu Nahel in Gaza City; the European Court of Human
Rights rules states may turn back migrants in "hybrid war" emergencies; a bus crash in Ras Al
Khaimah kills 13; and a car bomb at Colombia's Meta governor's office wounds 20+ on the eve of
the 10th anniversary of the 2016 peace deal.

See [REPORT.md](REPORT.md) for the six stories with their sources and dating notes.

This is an entry for the [make.fun bounty **news-image-20261124**](https://make.fun/bounty/news-image-20261124)
— "Sum up 24 November's world news in one image". The program is `main.ts` (Node 22,
standard library only): it copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Reproduce

```sh
python3 render.py   # draws entry.png (1024x1024, deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
