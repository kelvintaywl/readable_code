import collections
import functools

from service.file import File as FileService
from service.language import Language


class SourceCodeAnalysis:

    def __init__(self, dirpath, code_language):
        self.dirpath = dirpath
        self.code_language = code_language
        self.counter = self.analyse_files()

    def analyse_files(self):

        cnt = collections.Counter()
        for i, filepath in enumerate(
                FileService.get_filepaths(self.dirpath)
        ):
            if self.code_language.verify(filepath):
                sc = SourceCodeFileAnalysis(filepath, self.code_language)
                cnt.update(sc.words)

        for stopword in Language.STOPWORDS + self.code_language.STOPWORDS:
            del cnt[stopword]

        return collections.Counter({
            key: count
            for key, count in cnt.items()
            if not (key.isdigit() or len(key) <= 1)
        })

    def get_words(self, most_common=5):
        return self.counter.most_common(most_common)


class SourceCodeFileAnalysis:

    def __init__(self, filepath, code_language):
        self.filepath = filepath
        self.class_names = []
        self.function_names = []
        self.words = []

        self.parse(code_language)

    def parse(self, code_language):
        class_keyword = code_language.class_keyword
        function_keyword = code_language.function_keyword

        with open(self.filepath, 'r') as f:
            for i, line in enumerate(f):
                words = line.strip().split()
                counter = 0
                while counter < len(words):
                    try:
                        if words[counter] == class_keyword and counter + 1 < len(words):
                            self.class_names.append(words[counter + 1])
                        elif words[counter] == function_keyword and counter + 1 < len(words):
                            self.function_names.append(words[counter + 1])
                    except IndexError:
                        pass
                    else:
                        counter += 1

        words = [
            list(Language.tokenize(class_or_function))
            for class_or_function in self.class_names + self.function_names
        ]

        if words:
            words = functools.reduce(lambda x, y: x + y, words)
            self.words = collections.Counter(words)

    def get_words(self, most_commmon=5):
        return self.words.most_common(most_commmon)