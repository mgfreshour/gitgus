import os
import tempfile


def get_choice(choices: list) -> int:
    delimiter = "\n"
    choices_str = delimiter.join(map(str, choices))
    selection = []

    with tempfile.NamedTemporaryFile() as input_file:
        with tempfile.NamedTemporaryFile() as output_file:
            # Create a temp file with list entries as lines
            input_file.write(choices_str.encode("utf-8"))
            input_file.flush()

            # Invoke fzf externally and write to output file
            # TODO - make sure fzf is installed and in PATH
            os.system(f'fzf < "{input_file.name}" > "{output_file.name}"')

            # get selected options
            # TODO - currently only supports single selection
            with open(output_file.name, encoding="utf-8") as f:
                for line in f:
                    selection.append(line.strip("\n"))

    index = choices.index(selection[0])

    return index
