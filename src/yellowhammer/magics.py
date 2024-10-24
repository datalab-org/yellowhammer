"""
Magics to support LLM interactions in IPython/Jupyter.
Adapted from fperez/jupytee and jan-janssen/LangSim.
"""

import os

from IPython import get_ipython
from IPython.core.magic import (
    Magics,
    magics_class,
    line_cell_magic,
)
from IPython.core.magic_arguments import (
    magic_arguments,
    argument,
    parse_argstring,
)
from IPython.display import Markdown
from .llm import get_chain, code, ConversationalResponse
from .prompt import API_PROMPT


def get_output(messages, temp=0.1):
    env = os.environ
    agent_executor = get_chain(
        api_provider=env.get("LLM_PROVIDER", "OPENAI"),
        api_key=env.get("LLM_API_KEY"),
        api_model=env.get("LLM_MODEL", None),
        api_temperature=env.get("LLM_TEMP", temp),
    )

    return agent_executor.invoke({"context": API_PROMPT, "messages": messages})


# Class to manage state and expose the main magics
@magics_class
class DatalabMagics(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        self.messages = []

    # A datalab magic that returns a code block
    @magic_arguments()
    @argument(
        "prompt",
        nargs="*",
        help="""Prompt for code generation. When used as a line magic,
        it runs to the end of the line. In cell mode, the entire cell
        is considered the code generation prompt.
        """,
    )
    @argument(
        "-T",
        "--temp",
        type=float,
        default=0.0,
        help="""Temperature, float in [0,1]. Higher values push the algorithm
        to generate more aggressive/"creative" output. [default=0.1].""",
    )
    @line_cell_magic
    def llm(self, line, cell=None):
        """
        Chat with the LLM. Return either conversation or code.
        """
        args = parse_argstring(self.llm, line)  # self.llm is a bound method

        if cell is None:
            prompt = " ".join(args.prompt)
        else:
            prompt = cell

        self.messages.append(("human", prompt))
        response = get_output(self.messages).final_output

        if isinstance(response, ConversationalResponse):
            output = response.response
            self.messages.append(("ai", output))
            return Markdown(output)

        elif isinstance(response, code):
            output = response
            self.messages.append(("ai", output.prefix))
            cell_fill = output.imports + "\n" + output.code
            get_ipython().set_next_input(cell_fill)
            return Markdown(output.prefix)


# If testing interactively, it's convenient to %run as a script in Jupyter
if __name__ == "__main__":
    get_ipython().register_magics(DatalabMagics)
