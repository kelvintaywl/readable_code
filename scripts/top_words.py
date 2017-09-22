import argparse
import collections
import functools
import os
import os.path
import re


class Utils:

    FUNCTION_SIGNATURE_REGEX = re.compile('^([a-zA-Z0-9_^\(^:]+)[\(:].*$')

    STOPWORDS = [
        'a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also',
        'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at',
        'be', 'because', 'been', 'but', 'by',
        'can', 'cannot', 'could',
        'dear', 'did', 'do', 'does',
        'either', 'else', 'ever', 'every',
        'for', 'from',
        'get', 'got',
        'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however',
        'i', 'if', 'in', 'into', 'is', 'it', 'its',
        'just', 'least', 'let', 'like', 'likely',
        'may', 'me', 'might', 'most', 'must', 'my',
        'neither', 'no', 'nor', 'not',
        'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own',
        'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'set',
        'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they',
        'this', 'tis', 'to', 'too', 'twas', 'test',
        'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which',
        'while', 'who', 'whom', 'why', 'will', 'with', 'would',
        'yet', 'you', 'your'
    ]

    @staticmethod
    def tokenize(class_or_function_name):
        extract = Utils.FUNCTION_SIGNATURE_REGEX.match(
            class_or_function_name
        )

        if not extract:
            return []
        function_name = extract.group(1)
        return Utils.parse_snake_camel_cases(function_name)

    @staticmethod
    def parse_snake_camel_cases(conjugated_word):
        for possible_word in conjugated_word.split('_'):
            if not possible_word:
                continue
            counter = 1
            word_buffer = possible_word[0]
            while counter < len(possible_word):
                if not possible_word[counter].islower():
                    yield word_buffer.lower()
                    word_buffer = ''

                word_buffer += possible_word[counter]
                counter += 1
            if word_buffer:
                yield word_buffer.lower()

    @staticmethod
    def get_filepaths(dirpath='.'):

        for dpath, dirs, files in os.walk(dirpath):
            for name in files:
                filename = os.path.join(dpath, name)
                yield filename
            if not dirs:
                continue
            else:
                for d in dirs:
                    Utils.get_filepaths(os.path.join(dpath, d))


class PythonCode:

    class_keyword = 'class'
    function_keyword = 'def'

    STOPWORDS = [
        'init', 'iter', 'len', 'str', 'repr'
    ]


class PHPCode:

    class_keyword = 'class'
    function_keyword = 'function'

    STOPWORDS = [
        'construct'
    ]


class GoCode:

    class_keyword = 'type'
    function_keyword = 'func'

    STOPWORDS = []




class CodeLanguageFactory:

    @staticmethod
    def create(code_extension):
        if code_extension == 'php':
            return PHPCode()
        if code_extension == 'py':
            return PythonCode()
        if code_extension == 'go':
            return GoCode()

        raise ValueError('unsupported code language')


class SourceCode:

    def __init__(self, filepath, code_language):
        self.filepath = filepath
        self.class_names = []
        self.function_names = []
        self.words = None
        self.parse(code_language)

    @staticmethod
    def fancy_table_print(array_2d):
        print('Count\t| Word')
        print('----\t| -----')
        for word, count in array_2d:
            print('{}\t| {}'.format(count, word))


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
            list(Utils.tokenize(class_or_function))
            for class_or_function in self.class_names + self.function_names
        ]

        if words:
            words = functools.reduce(lambda x, y: x + y, words)
            self.words = collections.Counter(words)

    def get_words(self, most_commmon=5):
        return self.words.most_common(most_commmon)


def summarize(directory_path, code_language_str, top_n):
    overall = collections.Counter()
    code_language = CodeLanguageFactory.create(code_language_str)
    for i, filepath in enumerate(
        Utils.get_filepaths(directory_path)
    ):
        if filepath.endswith('.{}'.format(code_language_str)):
            sc = SourceCode(filepath, code_language)
            overall.update(sc.words)

    for stopword in Utils.STOPWORDS + code_language.STOPWORDS:
        del overall[stopword]

    for key in overall.keys():
        if key.isdigit() or len(key) <= 1:
            del overall[key]

    SourceCode.fancy_table_print(overall.most_common(top_n))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('directory', default='.')
    parser.add_argument('-l', '--code_language', choices=['php', 'py', 'go'])
    parser.add_argument('-n', '--max', default=5, type=int, help='show up to top N common words')

    args = parser.parse_args()

    summarize(args.directory, args.code_language, args.max)
