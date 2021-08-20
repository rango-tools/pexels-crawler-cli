# Pexels Crawler CLI
This is Simple CLI To Get Image With Specific Tag [Pexels](https://www.pexels.com/)


## Installation
First you need to install `Python v3.8` or upper after please install below packages with `pip`

```bash
pip install requests
pip install selenium
pip install docopt
```

## CLI Options
This is the list of this CLI options
```
--page-count=<count>                Page Counter, Default: 0 (All Pages)
--show-browser                      Showing Browser if You Need.
--load-time=<seconds>               Infinite Scroll Time Out, Deault: 5
-h --help                           Show this screen.
-v --version                        Show version.
```

## Example
Simple example for this CLI when you want to run.


```bash

# Search By Keyword
python pexels.py search [--options] "YOUR-KEYWORD"
```