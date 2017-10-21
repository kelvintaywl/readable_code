import logging
import os

from flask import Flask, jsonify, request

from service.storage import Storage as DataStore
from service.github import RepoInfo as GithubInfo, SourceCode as GithubSourceCode
from service.source_code_analysis import SourceCodeAnalysis


app = Flask(__name__)
app.config['redis_url'] = os.getenv('REDIS_URL', 'redis://localhost:6379')

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)
app.logger.addHandler(log_handler)


@app.route('/')
def hello_world():
    return """
    GET /github/:owner/:repo?top_n=10
    
    to fetch top 10 common words from variables and function names in your Github repo
    """


@app.route('/github/<owner>/<repo>')
def github_repo(owner, repo):

    num_top_n_words = int(request.args.get('top_n', 10))

    db = DataStore(app.config['redis_url'])
    key = '{}/{}'.format(owner, repo)

    repo_info = GithubInfo(owner, repo)

    try:
        words = db.get(key, num_top_n_words, last_updated=repo_info.last_updated)
        return jsonify(words)
    except LookupError:
        with GithubSourceCode(owner, repo) as source_code:
            analyser = SourceCodeAnalysis(source_code.code_dirpath, repo_info.code_language)

        words = analyser.get_words(num_top_n_words)
        db.set(key, words, num_top_n_words)

        return jsonify(words)
