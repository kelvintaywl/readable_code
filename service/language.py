import re


class Language:
    """ Collection of language-related helper functions """

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
        extract = Language.FUNCTION_SIGNATURE_REGEX.match(
            class_or_function_name
        )

        if not extract:
            return []
        function_name = extract.group(1)
        return Language.parse_snake_camel_cases(function_name)

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
