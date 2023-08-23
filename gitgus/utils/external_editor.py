import os
import tempfile


class ExternalEditor:
    def __init__(self, editor):
        if not editor:
            raise Exception("No editor provided. By default this is an environment variable called EDITOR.")
        self.editor = editor

    def edit(self, text):
        """Edit the given text using the external editor.

        :param text: The text to edit.
        :return: The edited text.
        """
        with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as f:
            f.write(text.encode("utf-8"))
            f.close()
        os.system("%s %s" % (os.getenv("EDITOR"), f.name))
        with open(f.name) as f:
            text = f.read()

        os.unlink(f.name)

        return text
