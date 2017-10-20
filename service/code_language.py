class CodeLanguageFactory:

    @staticmethod
    def create(code_language):
        code_language = code_language.lower()
        if code_language == 'php':
            return PHPCode()
        if code_language == 'python':
            return PythonCode()
        if code_language in ('go', 'golang'):
            return GoCode()

        raise ValueError('unsupported code language')


class BaseCodeLanguage:

    def verify(self, filepath):
        return filepath.endswith(self.extension)


class PythonCode(BaseCodeLanguage):

    class_keyword = 'class'
    function_keyword = 'def'

    STOPWORDS = [
        'init', 'iter', 'len', 'str', 'repr'
    ]

    extension = '.py'


class PHPCode(BaseCodeLanguage):

    class_keyword = 'class'
    function_keyword = 'function'

    STOPWORDS = [
        'construct'
    ]

    extension = '.php'


class GoCode(BaseCodeLanguage):

    class_keyword = 'type'
    function_keyword = 'func'

    STOPWORDS = []

    extension = '.go'
