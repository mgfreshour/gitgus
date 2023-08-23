from gitgus.utils.HTMLStripper import strip_tags


def test_strip_tags():
    tests = [
        (
            "<p>Some text</p>",
            "Some text\n",
        ),
        (
            "<p>Some text</p><p>Some <em>more text</em></p>",
            "Some text\nSome \n_more text_",
        ),
        (
            "<p>Some text</p><ul><li>Some more text</li><li>And even more text</li></ul><p>And even more text</p>",
            "Some text\n- Some more text\n- And even more text\nAnd even more text\n",
        ),
        (
            '<p>hello <a href="https://www.google.com">world</a></p>',
            "hello \nworld (https://www.google.com)",
        ),
    ]
    for html, expected in tests:
        actual = strip_tags(html)
        assert actual == expected
