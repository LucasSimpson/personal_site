import re
from typing import Tuple, Iterable

TextCaptureGroup = Tuple[int, int, str]  # start index, end index, text


class TextCapture:
    """
    Primitively, takes in a bunch of text and spits out capture groups
    Base method is capture(str) -> Iterable[TextCaptureGroup]
    """

    def capture(self, text: str) -> Iterable[TextCaptureGroup]:
        return []


class SplitCapture(TextCapture):
    """
    Just splits the text on a substring.
    """

    def __init__(self, split_substring: str):
        self.split_substring = split_substring

    def capture(self, text: str):
        start_index = 0

        for match in re.finditer(self.split_substring, text):
            yield [start_index, match.start(), text[start_index:match.start()]]
            start_index = match.end()

        yield[start_index, len(text), text[start_index:]]


class TokenEnclosedCapture(TextCapture):
    """
    Captures text based on a [start] and [end] token.
    """

    @staticmethod
    def _find_distance(text: str, token: str) -> int:
        for i, char in enumerate(text):
            if char == token:
                return i
        return len(text)

    @staticmethod
    def _to_safe_regex(pattern: str) -> str:
        unsafe_chars = '[]().|^*'
        res = pattern
        for char in unsafe_chars:
            if char in res:
                res = res.replace(char, f'\\{char}')
        return res

    def __init__(self, start_token: str, end_token: str):
        self.start_token = start_token
        self.end_token = end_token

    def capture(self, text: str) -> Iterable[TextCaptureGroup]:
        regex = r'[^a-zA-Z0-9]' + \
                TokenEnclosedCapture._to_safe_regex(self.start_token) + \
                r'.+?' + \
                TokenEnclosedCapture._to_safe_regex(self.end_token) + \
                r'[^a-zA-Z0-9]'

        for match in re.finditer(regex, text):
            reg_start, reg_end = match.start(), match.end()
            full_match = text[reg_start:reg_end]
            start_distance = TokenEnclosedCapture._find_distance(full_match, self.start_token)
            end_distance = TokenEnclosedCapture._find_distance(''.join(reversed(full_match)), self.end_token)

            yield [reg_start + start_distance, reg_end - end_distance, full_match[start_distance: -end_distance]]



