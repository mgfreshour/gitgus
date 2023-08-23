from io import StringIO
from html.parser import HTMLParser


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        if self._HTMLParser__starttag_text:
            if self._HTMLParser__starttag_text == "<li>":
                self.text.write("- ")
            if self._HTMLParser__starttag_text[:7] == "<strong":
                self.text.write("*")
            if self._HTMLParser__starttag_text[:4] == "<em>":
                self.text.write("_")

        self.text.write(d)

        if self._HTMLParser__starttag_text:
            if self._HTMLParser__starttag_text[:7] == "<a href":
                url = self._HTMLParser__starttag_text.split('"')[1]
                if url:
                    self.text.write(f" ({url})")
            if self._HTMLParser__starttag_text[:7] == "<strong":
                self.text.write("*")
            elif self._HTMLParser__starttag_text[:4] == "<em>":
                self.text.write("_")
            elif self._HTMLParser__starttag_text == "<li>" or self._HTMLParser__starttag_text == "<p>":
                self.text.write("\n")

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    if not html:
        return ""
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()
