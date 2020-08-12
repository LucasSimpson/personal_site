from blog.formatting.text_capture import TextCapture, TokenEnclosedCapture, SplitCapture
from blog.formatting.transformers import Transformer, HTMLTagWrapperTransformer, ReplaceLR, LinkTransformer


class Formatter:
    """
    Combine a TextCapture and a Transformer to create a formatter.
    Usage is through format(str) -> str.
    """

    @staticmethod
    def chain(formatters):
        """Chain together a list of formatters into 1."""
        return ChainedFormatter(formatters)

    def __init__(self, limit_to: int=-1):
        self.limit_to = limit_to

    def format(self, text: str) -> str:
        text_capture = self.get_text_capture()
        transformer = self.get_transformer()
        result_text = ''
        position = 0
        num_captures = 0

        for start_index, end_index, captured_text in text_capture.capture(text):
            result_text += text[position:start_index]
            result_text += transformer.transform(captured_text)
            position = end_index

            num_captures += 1
            if num_captures == self.limit_to:
                return result_text

        result_text += text[position:]

        return result_text

    def get_text_capture(self) -> TextCapture:
        if hasattr(self, 'text_capture') and self.text_capture is not None:
            return self.text_capture

        raise Exception(f'{self.__class__} must implement a text capture')

    def get_transformer(self) -> Transformer:
        if hasattr(self, 'transformer') and self.transformer is not None:
            return self.transformer

        raise Exception(f'{self.__class__} must implement a transformer')


class ChainedFormatter(Formatter):
    def __init__(self, formatters):
        self.formatters = formatters

    def format(self, text: str) -> str:
        result = text
        for formatter in self.formatters:
            result = formatter.format(result)
        return result


class ChoiceFormatter(Formatter):
    """
    Takes two formatters and a conditional.
    uses the first formatter if the condition is met,
    otherwise uses the second
    """

    def __init__(self, limit_to: int=-1):
        super().__init__(limit_to)
        self._first_formatter = self.get_first_formatter()
        self._second_formatter = self.get_second_formatter()
        self._cond_func = self.get_cond_func()

    def format(self, text: str) -> str:
        if self._cond_func(text):
            self._first_formatter.limit_to = self.limit_to
            return self._first_formatter.format(text)
        else:
            self._second_formatter.limit_to = self.limit_to
            return self._second_formatter.format(text)

    def get_first_formatter(self) -> Formatter:
        if hasattr(self, 'first_formatter') and self.first_formatter is not None:
            return self.first_formatter

        raise Exception(f'{self.__class__} must implement a first_formatter')

    def get_second_formatter(self) -> Formatter:
        if hasattr(self, 'second_formatter') and self.second_formatter is not None:
            return self.second_formatter

        raise Exception(f'{self.__class__} must implement a second_formatter')

    def get_cond_func(self):
        if hasattr(self, 'cond_func') and self.cond_func is not None:
            return self.cond_func

        raise Exception(f'{self.__class__} must implement a cond_func')


class ToParagraphs(Formatter):
    text_capture = SplitCapture('  ')
    transformer = HTMLTagWrapperTransformer('p')


class HTMLParagraphs(Formatter):
    text_capture = SplitCapture('<p>')
    transformer = Transformer()


class ParagraphChoiceFormatter(ChoiceFormatter):
    first_formatter = HTMLParagraphs()
    second_formatter = ToParagraphs()
    cond_func = lambda _, text: text[0] == '<'  # probably HTML content


class ToItalics(Formatter):
    text_capture = TokenEnclosedCapture('_', '_')
    transformer = ReplaceLR('_', '<i>', '</i>')


class ToBold(Formatter):
    text_capture = TokenEnclosedCapture('*', '*')
    transformer = ReplaceLR('*', '<b>', '</b>')


class Linkify(Formatter):
    text_capture = TokenEnclosedCapture('[', ']')
    transformer = LinkTransformer()
