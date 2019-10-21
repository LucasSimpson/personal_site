from blog.formatting.text_capture import TextCapture, TokenEnclosedCapture, SplitCapture
from blog.formatting.transformers import Transformer, HTMLTagWrapperTransformer, ReplaceLR, LinkTransformer


class Formatter:
    """
    Combine a TextCapture and a Transformer to create a formatter.
    Usage is through format(str) -> str.
    """

    def format(self, text: str) -> str:
        text_capture = self.get_text_capture()
        transformer = self.get_transformer()
        result_text = ''
        position = 0

        for start_index, end_index, captured_text in text_capture.capture(text):
            result_text += text[position:start_index]
            result_text += transformer.transform(captured_text)
            position = end_index

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


class ToParagraphs(Formatter):
    text_capture = SplitCapture('  ')
    transformer = HTMLTagWrapperTransformer('p')


class ToItalics(Formatter):
    text_capture = TokenEnclosedCapture('_', '_')
    transformer = ReplaceLR('_', '<i>', '</i>')


class ToBold(Formatter):
    text_capture = TokenEnclosedCapture('*', '*')
    transformer = ReplaceLR('*', '<b>', '</b>')


class Linkify(Formatter):
    text_capture = TokenEnclosedCapture('[', ']')
    transformer = LinkTransformer()
