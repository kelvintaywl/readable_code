import collections
import functools

from pygments.token import Token

from service.file import File as FileService
from service.language import Language


class SourceCodeAnalysis:

    def __init__(self, dirpath, code_language):
        self.dirpath = dirpath
        self.code_language = code_language
        self.lexer = self.code_language.LexerClass()
        self.counter = self.analyse_files()


    def analyse_files(self):

        cnt = collections.Counter()
        for i, filepath in enumerate(
                FileService.get_filepaths(self.dirpath)
        ):
            if self.code_language.verify(filepath):
                sc = SourceCodeFileAnalysis(filepath, self.lexer)
                cnt.update(sc.words)

        for stopword in Language.STOPWORDS:
            del cnt[stopword]

        return collections.Counter({
            key: count
            for key, count in cnt.items()
            if not (key.isdigit() or len(key) <= 1)
        })

    def get_words(self, most_common=5):
        return self.counter.most_common(most_common)


class SourceCodeFileAnalysis:

    def __init__(self, filepath, lexer):
        self.filepath = filepath
        self.class_names = []
        self.function_names = []
        self.words = []

        self.parse(lexer)

    def parse(self, lexer):
        total_words = []
        with open(self.filepath, 'r') as f:
            tokens = lexer.get_tokens(f.read())
            for TokenClass, conjugated_word in tokens:
                if TokenClass in (Token.Name.Function, Token.Name, Token.Name.Class):
                    words = Language.parse_snake_camel_cases(conjugated_word)
                    words = [
                        Language.singular(word)
                        for word in words
                    ]
                    total_words.append(words)
        if total_words:
            total_words = functools.reduce(lambda x, y: x + y, total_words)

        self.words = collections.Counter(total_words)

    def get_words(self, most_commmon=5):
        return self.words.most_common(most_commmon)