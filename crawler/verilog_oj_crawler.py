import requests
import loguru
from tqdm import tqdm
import os, sys
from pathlib import Path
import concurrent.futures
import json
import mistletoe.markdown_renderer


class MDVParser(mistletoe.markdown_renderer.MarkdownRenderer, requests.Session):
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

    def to_md(self, problem_data: dict, dest: Path):         
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

    def to_v(self, problem_data: dict, dest: Path):
        if not os.path.exists(dest.as_posix()):
            os.makedirs(dest.as_posix(), exist_ok=True)
        v = f'/*\n'
        v += f' * id: {problem_data["id"]}\n'
        v += f' * logic_id: {problem_data["logic_id"]}\n'
        v += f' * name: {problem_data["name"]}\n'
        v += f' * level: {problem_data["level"]}\n'
        v += f' * tags: {problem_data["tags"]}\n'
        v += f' * points: {problem_data["points"]}\n'
        v += f' * answer_id: {problem_data["answer_id"]}\n'
        v += f' * answer_file_id: {problem_data["answer_file_id"]}\n'
        v += f' */\n\n'
        v += problem_data["answer"]
        with open((dest / 'answer.v').as_posix(), 'w', encoding='utf-8') as f:
            f.write(v)
        return v


class VerilogOJCrawler(requests.Session):
    def __init__(
        self, 
        base_url, 
        get_answer=False,
        **kwargs
    ):
        """
        The crawler for Verilog OJ.
        
        ### Args:
        - `base_url`: str, the base url of the OJ, should be like http://xxx.xxx.xxx.xxx/oj
        - `get_answer`: bool, whether to get the answer of the problems
        - `**kwargs`: 
          - `username`: str, the username of the OJ (needed if `get_answer` is True)
          - `password`: str, the password of the OJ (needed if `get_answer` is True)
          - `log_file`: str, the log file path (default: None)
        """
        super(VerilogOJCrawler, self).__init__()
        self.base_url = base_url
        self.logger = loguru.logger
        log_file = kwargs.get('log_file', None)
        if log_file is not None:
            os.makedirs(Path(log_file).parent.as_posix(), exist_ok=True)
        else:
            os.makedirs((Path(__file__).parent / 'log').as_posix(), exist_ok=True)
        self.logger.remove()
        self.logger.add(log_file if log_file is not None else (Path(__file__).parent / 'log/crawler.log').as_posix(), rotation='5 MB')
        self.logger.add(sys.stderr, level='INFO')
        self.md_parser = MDVParser(self.logger)
        self.logger.info('Crawler started.')
        self.user_id = None
        if get_answer:
            username, password = kwargs.get('username', None), kwargs.get('password', None)
            if username is None or password is None:
                self.logger.error('Username and password are needed to get answers.')
                raise ValueError('Username and password are needed to get answers.')
            if not self.login(username, password):
                raise ValueError('Failed to login.')
            self.logger.info('Login success.')
        self.logger.info('Crawler initialized.')
        self.problems, self.answers = {}, {}
        self.crawled_problems, self.crawled_answers = set(), set()
        
        
    def login(self, username: str, password: str):
        resp = self.post(f"{self.base_url}/api/user/login", data={'username': username, 'password': password})
        if not resp.ok:
            self.logger.error(f'Failed to login: {resp.text}')
            return False
        resp = self.get(f"{self.base_url}/api/user/status-login")
        if not resp.ok:
            self.logger.error(f'Failed to check login status: {resp.text}')
            return False
        data = resp.json()
        if data['isLoggedIn']:
            self.logger.info(f'Login success: {data["username"]}')
            self.user_id = data['userID']
            return True
        else:
            self.logger.error(f'Login failed: {data["username"]}')
            return False

    
    def get_all(self, dest='problems', workers=1):
        dest = Path(dest)
        os.makedirs(dest.as_posix(), exist_ok=True)
        if not os.path.exists((dest / 'crawled.json').as_posix()):
            with open((dest / 'crawled.json').as_posix(), 'w', encoding='utf-8') as f:
                f.write(json.dumps({
                    'crawled_problems': [],
                    'crawled_answers': []
                }))
        else:
            with open((dest / 'crawled.json').as_posix(), 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.crawled_problems = set(data['crawled_problems'])
                self.crawled_answers = set(data['crawled_answers'])
         
        # get problem list   
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
                self.problems[prob['logic_id']] = {
                    'id': prob['id'],
                    'logic_id': prob['logic_id'],
                    'name': prob['name'],
                    'level': prob['level'],
                    'tags': prob['tags'],
                    'points': prob['total_grade'],
                }
        
        # get problem details        
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            tasks = [executor.submit(self.get_problem, prob) for logic_id, prob in self.problems.items() if logic_id not in self.crawled_problems]
            pbar = tqdm(total=len(tasks), ncols=100, ascii=True)
            pbar.set_description('Getting problem logic_id: None')
            for task in concurrent.futures.as_completed(tasks):
                data = task.result()
                if data is None:
                    pbar.update(1)
                    continue
                self.problems[data['logic_id']].update(data)
                pbar.set_description(f'Getting problem logic_id: {data["logic_id"]}')
                md = self.md_parser.to_md(data, dest / f'{data["logic_id"]}-{data["name"]}')
                if md:
                    self.crawled_problems.add(data['logic_id'])
                else:
                    self.logger.error(f'Failed to save problem {data["logic_id"]}')
                pbar.update(1)
            pbar.close()
        with open((dest / 'crawled.json').as_posix(), 'w', encoding='utf-8') as f:
            json.dump({
                'crawled_problems': list(self.crawled_problems),
                'crawled_answers': list(self.crawled_answers)
            }, f)
            
        # get answers
        if self.get_answer:
            resp = self.get(f'{self.base_url}/api/users/{self.user_id}')
            if not resp.ok:
                self.logger.error(f'Failed to get answer list from user info: {resp.text}')
                return
            self.answers = {acp['logic_id']: self.problems[acp['logic_id']] for acp in resp.json()['ac_problems']}
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                tasks = [executor.submit(self.get_answer, prob) for logic_id, prob in self.answers.items() if logic_id not in self.crawled_answers]
                pbar = tqdm(total=len(tasks), ncols=100, ascii=True)
                pbar.set_description('Getting answer logic_id: None')
                for task in concurrent.futures.as_completed(tasks):
                    data = task.result()
                    if data is None:
                        pbar.update(1)
                        continue
                    self.answers[data['logic_id']] = data
                    pbar.set_description(f'Getting answer logic_id: {data["logic_id"]}')
                    v = self.md_parser.to_v(data, dest / f'{data["logic_id"]}-{data["name"]}')
                    if v:
                        self.crawled_answers.add(data['logic_id'])
                    else:
                        self.logger.error(f'Failed to save answer {data["logic_id"]}')
                    pbar.update(1)
                pbar.close()
        with open((dest / 'crawled.json').as_posix(), 'w', encoding='utf-8') as f:
            json.dump({
                'crawled_problems': list(self.crawled_problems),
                'crawled_answers': list(self.crawled_answers)
            }, f)
            
        return self.problems, self.answers

    
    def get_problem(self, problem):
        resp = self.get(f'{self.base_url}/api/problems/{problem["id"]}/')
        if not resp.ok:
            self.logger.error(f'Failed to get problem {problem["logic_id"]}: {resp.text}')
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


    def get_answer(self, problem):
        resp = self.get(f'{self.base_url}/api/submissions/?user={self.user_id}&problem={problem["id"]}')
        if not resp.ok:
            self.logger.error(f'Failed to get answer {problem["logic_id"]}: {resp.text}')
            return None
        data = resp.json()
        if len(data) == 0:
            self.logger.error(f'No answer for problem {problem["logic_id"]}')
            return None
        ac_submission = [sub for sub in data if sub['result'] == 'Accepted']
        if len(ac_submission) == 0:
            self.logger.error(f'No accepted answer for problem {problem["logic_id"]}')
            return None
        problem.update({'answer_id': ac_submission[0]['id']})
        resp = self.get(f'{self.base_url}/api/submissions/{problem["answer_id"]}')
        if not resp.ok:
            self.logger.error(f'Failed to get answer {problem["logic_id"]}: {resp.text}')
            return None
        problem.update({'answer_file_id': resp.json()['submit_file']})
        resp = self.get(f'{self.base_url}/api/files/{problem["answer_file_id"]}')
        if not resp.ok:
            self.logger.error(f'Failed to get answer file {problem["answer_file_id"]}: {resp.text}')
            return None
        problem.update({'answer': resp.text.replace('\r\n', '\n')})
        return problem

    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True, help='the url of the OJ, should be like http://xxx.xxx.xxx.xxx/oj')
    parser.add_argument('--log', '-l', type=str, required=False, help='the log file path', default=None)
    parser.add_argument('--dest', '-d', type=str, required=False, help='the destination directory to save problems', default='problems')
    parser.add_argument('--workers', '-w', type=int, required=False, help='the number of workers to crawl problems', default=4)
    parser.add_argument('--get_answer', '-a', action='store_true', help='whether to get the answer of the problems (default: False)', default=False)
    parser.add_argument('--username', '-u', type=str, required=False, help='the username of the OJ (needed if `get_answer` is True)', default=None)
    parser.add_argument('--password', '-p', type=str, required=False, help='the password of the OJ (needed if `get_answer` is True)', default=None)
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        exit(0)
    
    # remove the final '/' if exists
    while args.url[-1] == '/':
        args.url = args.url[:-1]
    
    crawler = VerilogOJCrawler(
        args.url, 
        get_answer=args.get_answer, 
        username=args.username, 
        password=args.password, 
        log_file=args.log
    )
    problems, answers = crawler.get_all(args.dest, args.workers)
