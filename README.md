# Pexels Crawler CLI
This is Simple CLI To Get Image With Specific Tag [Pexels](https://www.pexels.com/)


## Installation

### Prerequisites
First you need to install `Python v3.x` or upper after that you need to setup the `chrome driver` for Selenium Library.

```bash
python3 -m pip install git+https://github.com/rango-tools/pexels-crawler-cli
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