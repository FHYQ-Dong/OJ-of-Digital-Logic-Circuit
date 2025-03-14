# Verilog OJ Crawler

Used to crawl problems from THU-EE-Verilog-OJ.

## Usage

1. Install requirements

```bash
pip install -r requirements.txt
```

2. Run the script
  - If you only want to crawl all the problems:
```bash
# Run in the parent directory of crawler/
python crawler/verilog_oj_crawler.py --url <url_to_oj> -d .
```
  - If you want to crawl all problems and your AC-answers (only one AC-answer per problem will be crawled):
```bash
# Run in the parent directory of crawler/
python crawler/verilog_oj_crawler.py --url <url_to_oj> -d . -a -u <your_oj_username> -p <your_oj_password>
```

3. You will find some folders under the parent directory of `crawler/` (can be changed through argument `--dest`/`-d`). Each folder contains one problem.

4. If you want to re-crawl the problems, remove `crawled.json` under the parent directory of `crawler/` (the directory specified through `--dest`/`-d`).
