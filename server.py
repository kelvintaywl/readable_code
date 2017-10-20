from flask import Flask, jsonify, request

from service.storage import Storage as DataStore
from service.github import Github as GithubService
from service.source_code_analysis import SourceCodeAnalysis


app = Flask(__name__)


@app.route('/')
def hello_world():
    return """
    GET /github/:owner/:repo?top_n=10
    
    to fetch top 10 common words from variables and function names in your Github repo
    """


@app.route('/github/<owner>/<repo>')
def github_repo(owner, repo):

    num_top_n_words = int(request.args.get('top_n', 10))

    db = DataStore()
    key = '{}/{}'.format(owner, repo)

    try:
        words = db.get(key, num_top_n_words)
        return jsonify(words)
    except LookupError:
        with GithubService(owner, repo) as github:
            analyser = SourceCodeAnalysis(github.code_dirpath, github.code_language)

        words = analyser.get_words(num_top_n_words)
        db.set(key, words, num_top_n_words)

        return jsonify(words)
