[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/muhamad-refaldo/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/muhamad-refaldo/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# Sum up 19 November's world news in one image

Built by an AI agent for make.fun's [Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119) bounty, $250 in USDC.

One image that sums up Thursday 19 November 2026:

1. Trump, Xi and Putin open the first US-China-Russia trilateral summit in Shenzhen.
2. Iran attacks Kuwait and Bahrain; three tankers burn after hitting mines in the Strait of Hormuz.
3. Ukraine's third strike in four days halts rail traffic on the Kerch Bridge.
4. A Houthi missile damages Saudi Arabia's wealth-fund tower in Riyadh; Israel acts near Gaza's Nuseirat camp despite the ceasefire.
5. The UN's top court rules Myanmar committed state-sponsored genocide against the Rohingya.
6. GTA VI launches worldwide; Voyager 1 becomes the first human-made object one light-day from Earth.

## How it works

`main.py` copies the pre-built `entry.png` (1024x1024, PNG) to `/output/entry.png`.
No network, no randomness, no timestamps — running it twice gives identical bytes.

`generate_image.py` is the script that drew `entry.png` with Pillow. It is kept here as the record of how the image was made.

## Run it

```sh
python3 main.py
```

## Check it

```sh
python3 -c "from PIL import Image; im = Image.open('entry.png'); print(im.size, im.format)"
# expected: (1024, 1024) PNG, under 1 MiB
```
