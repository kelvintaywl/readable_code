from pygments.lexers import (
    GoLexer,
    PhpLexer,
    PythonLexer,
    RubyLexer,
    JavascriptLexer
)


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
        if code_language == 'ruby':
            return RubyCode()
        if code_language == 'javascript':
            return JavascriptCode()

        raise ValueError('unsupported code language')


class BaseCodeLanguage:

    LexerClass = None

    def verify(self, filepath):
        return filepath.endswith(self.extension)


class JavascriptCode(BaseCodeLanguage):

    LexerClass = JavascriptLexer
    extension = '.js'


class RubyCode(BaseCodeLanguage):

    LexerClass = RubyLexer
    extension = '.rb'


class PythonCode(BaseCodeLanguage):

    LexerClass = PythonLexer
    extension = '.py'


class PHPCode(BaseCodeLanguage):

    LexerClass = PhpLexer
    extension = '.php'


class GoCode(BaseCodeLanguage):

    LexerClass = GoLexer
    extension = '.go'
