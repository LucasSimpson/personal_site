class Transformer:
    """
    Primitively, defines a transformation of str -> str.
    Base method is the transform(str) -> str.
    """

    def transform(self, text: str) -> str:
        return text

    def chain(self, other):
        """Return a new transformer being the combination of sending the output of {self} into {other}"""
        return ChainedTransformer(self, other)


class ChainedTransformer(Transformer):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def transform(self, text: str):
        return self.second.transform(self.first.transform(text))


class HTMLTagWrapperTransformer(Transformer):
    def __init__(self, html_tag: str):
        self.html_tag = html_tag

    def transform(self, text: str):
        return f'<{self.html_tag}>{text.strip()}</{self.html_tag}>'


class ReplaceLR(Transformer):
    """Searches from both left and right for a given token and removes it."""

    def __init__(self, token: str, replace_left: str, replace_right: str):
        self.token = token
        self.replace_left = replace_left
        self.replace_right = replace_right

    def _smart_rem(self, text: str, replacement: str) -> str:
        for i, char in enumerate(text):
            if char == self.token:
                return text[:i] + replacement + text[i + 1:]
        return text

    def transform(self, text: str) -> str:
        result = self._smart_rem(text, self.replace_left)

        result = ''.join(reversed(result))
        result = self._smart_rem(result, ''.join(reversed(self.replace_right)))
        result = ''.join(reversed(result))

        return result


class LinkTransformer(Transformer):
    def transform(self, text: str):
        text, url = text.split('|')
        return f'<a href="{url[:-1]}">{text[1:]}</a>'

