import requests
import loguru
from tqdm import tqdm
import os
from pathlib import Path
import concurrent.futures
import json
import mistletoe.markdown_renderer


class MDParser(mistletoe.markdown_renderer.MarkdownRenderer, requests.Session):
    def __init__(self, logger):
        mistletoe.markdown_renderer.MarkdownRenderer.__init__(self)
        requests.Session.__init__(self)
        self.logger = logger
        
    def get_img_recursive(self, token, dest: Path):
        if token.__class__.__name__ == 'Image':
            img_name = Path(token.src).name
            resp = self.get(token.src)
            if not resp.ok:
                raise requests.HTTPError(f'Failed to get image {token.src}: {resp.text}')
            with open((dest / 'assets' / img_name).as_posix(), 'wb') as f:
                f.write(resp.content)
            token.src = (Path('assets') / Path(token.src).name).as_posix()
            token.children[0].content = img_name
        for i, child in enumerate(token.children):
            if child.children is not None:
                self.get_img_recursive(token.children[i], dest)

    def to_markdown(self, problem_data: dict, dest: Path):         
        if not os.path.exists((dest / 'assets').as_posix()):
            os.makedirs((dest / 'assets').as_posix(), exist_ok=True)
        md = '---\n'
        md += f'id: {problem_data["id"]}\n'
        md += f'logic_id: {problem_data["logic_id"]}\n'
        md += f'name: {problem_data["name"]}\n'
        md += f'level: {problem_data["level"]}\n'
        md += f'tags: {problem_data["tags"]}\n'
        md += f'points: {problem_data["points"]}\n'
        md += '---\n\n'
        md += f'# {problem_data["name"]}\n\n'
        md += f'## 题目描述\n{problem_data["description"]}\n\n'
        md += f'## 输入格式\n{problem_data["input"]}\n\n'
        md += f'## 输出格式\n{problem_data["output"]}\n\n'
        md += f'## 代码\n```verilog\n{problem_data["template_code"]}\n```\n'

        md = mistletoe.Document(md)
        try:
            self.get_img_recursive(md, dest)
        except Exception as e:
            self.logger.error(f'Failed to get images for problem {problem_data["logic_id"]}: {e}')
            return None
        md = self.render(md)
        with open((dest / 'problem.md').as_posix(), 'w', encoding='utf-8') as f:
            f.write(md)
        return md

class VerilogOJCrawler(requests.Session):
    def __init__(
        self, 
        base_url, 
        log_file=None
    ):
        super(VerilogOJCrawler, self).__init__()
        self.base_url = base_url
        self.logger = loguru.logger
        self.logger.add(log_file if log_file is not None else (Path(__file__).parent / 'log/crawler.log').as_posix(), rotation='5 MB')
        self.md_parser = MDParser(self.logger)
        self.logger.info('Crawler started.')
        
    
    def get_all_problems(self, dest='problems', workers=1):
        dest = Path(dest)
        crwaled_problems = []
        os.makedirs(dest.as_posix(), exist_ok=True)
        if not os.path.exists((dest / 'crwaled_problems.json').as_posix()):
            with open((dest / 'crwaled_problems.json').as_posix(), 'w', encoding='utf-8') as f:
                f.write('[]')
        crwaled_problems = set(json.load(open((dest / 'crwaled_problems.json').as_posix(), 'r', encoding='utf-8')))
            
        problems = []
        resp = self.get(f'{self.base_url}/api/problems/?limit=15&offset=0')
        if not resp.ok:
            self.logger.error(f'Failed to get problems: {resp.text}')
            return
        data = resp.json()
        problem_cnt = data['count']
        for offset in (pbar := tqdm(range(0, problem_cnt, 15), ncols=100, ascii=True)):
            pbar.set_description(f'Getting problems {offset}-{offset+15}')
            resp = self.get(f'{self.base_url}/api/problems/?limit=15&offset={offset}')
            if not resp.ok:
                self.logger.error(f'Failed to get problems {offset}-{offset+15}: {resp.text}')
                return
            data = resp.json()
            for prob in data['results']:
                problems.append({
                    'id': prob['id'],
                    'logic_id': prob['logic_id'],
                    'name': prob['name'],
                    'level': prob['level'],
                    'tags': prob['tags'],
                    'points': prob['total_grade'],
                })
                
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            tasks = [executor.submit(self.get_problem, prob) for prob in problems if prob['logic_id'] not in crwaled_problems]
            problems = []
            pbar = tqdm(total=len(tasks), ncols=100, ascii=True)
            for task in concurrent.futures.as_completed(tasks):
                data = task.result()
                if data is None:
                    pbar.update(1)
                    continue
                problems.append(data)
                pbar.set_description(f'Getting problem id: {data["logic_id"]}')
                md = self.md_parser.to_markdown(data, dest / f'{data["logic_id"]}-{data["name"]}')
                if md:
                    crwaled_problems.add(data['logic_id'])
                else:
                    self.logger.error(f'Failed to save problem {data["logic_id"]}')
                pbar.update(1)
            pbar.close()
        with open((dest / 'crwaled_problems.json').as_posix(), 'w', encoding='utf-8') as f:
            json.dump(list(crwaled_problems), f)
        return problems

    
    def get_problem(self, problem):
        resp = self.get(f'{self.base_url}/api/problems/{problem["id"]}/')
        if not resp.ok:
            self.logger.error(f'Failed to get problem {problem["id"]}: {resp.text}')
            return None
        data = resp.json()
        problem.update({
            'description': data['description'].replace('\r\n', '\n'),
            'input': data['description_input'].replace('\r\n', '\n'),
            'output': data['description_output'].replace('\r\n', '\n'),
            'template_code_file': data['template_code_file']
        })
        resp = self.get(f'{self.base_url}/api/files/{data["template_code_file"]}')
        if not resp.ok:
            self.logger.error(f'Failed to get template code file {data["template_code_file"]}: {resp.text}')
            return None
        problem.update({'template_code': resp.text.replace('\r\n', '\n')})
        return problem




    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', type=str, required=True, help='the url of the OJ, should be like http://xxx.xxx.xxx.xxx/oj')
    parser.add_argument('--log', '-l', type=str, required=False, help='the log file path', default=None)
    parser.add_argument('--dest', '-d', type=str, required=False, help='the destination directory to save problems', default='problems')
    parser.add_argument('--workers', '-w', type=int, required=False, help='the number of workers to crawl problems', default=4)
    args = parser.parse_args()
    
    crawler = VerilogOJCrawler(args.url, args.log)
    problems = crawler.get_all_problems(args.dest, args.workers)
