# Verilog OJ Crawler

Used to crawl problems from THU-EE-Verilog-OJ.

## Usage

1. Install requirements

```bash
pip install -r requirements.txt
```

2. Run the script

```bash
# Run in the parent directory of crawler/
python crawler/verilog_oj_crawler.py -u <url_to_oj> -d .
```

3. You will find some folders under the parent directory of `crawler/`. Each folder contains one problem (of course, no answers).
4. If you want to re-crawl the problems, remove `crwaled_problems.json` under the parent directory of `crawler/`.
