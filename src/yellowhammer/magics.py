"""
Magics to support LLM interactions in IPython/Jupyter.
Adapted from fperez/jupytee and jan-janssen/LangSim.
"""

import os
import re
import base64

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
from langchain_core.prompts import ChatPromptTemplate
from .llm import get_chain, Code, ConversationalResponse
from .prompt import API_PROMPT, SYSTEM_PROMPT


def get_output(messages, image_dict, temp=0.1):
    """
    Send current message list to LLM and return the response
    """

    env = os.environ

    # Convert list of tuples to ChatPromptTemplate
    messages = ChatPromptTemplate(messages)

    agent_executor = get_chain(
        messages=messages,
        api_provider=env.get("LLM_PROVIDER", "OPENAI"),
        api_key=env.get("LLM_API_KEY"),
        api_model=env.get("LLM_MODEL", None),
        api_temperature=env.get("LLM_TEMP", temp),
    )

    # Add image data to LLM input as key-value pairs
    args = {"context": API_PROMPT}
    args.update(image_dict)

    return agent_executor.invoke(args)


def parse_paths(input_string):
    # A simple regex pattern to match file-path-like substrings:
    # [A-Za-z0-9_.\\/-]+\.[A-Za-z0-9_]+
    #    - one or more letters, digits, underscores, dots, slashes, or dashes,
    #      containing at least one dot that leads to a plausible extension
    file_path_pattern = r"([A-Za-z0-9_.\\/-]+\.[A-Za-z0-9_]+)"

    # Find all file paths
    paths = re.findall(file_path_pattern, input_string)

    # Remove those file paths from the original string
    remaining_text = re.sub(file_path_pattern, "", input_string)

    # Clean up extra whitespace
    remaining_text = re.sub(r"\s+", " ", remaining_text).strip()

    return {"text": remaining_text, "paths": paths}


# Class to manage state and expose the main magics
@magics_class
class DatalabMagics(Magics):
    def __init__(self, shell):
        super().__init__(shell)

        self.messages = [
            ("system", SYSTEM_PROMPT),
        ]  # Initialize with system prompt.
        self.images = []  # Initialize with empty list of images.

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
        default=0.1,
        help="""Temperature, float in [0,1]. Higher values push the algorithm
        to generate more aggressive/"creative" output. [default=0.1].""",
    )
    @line_cell_magic
    def llm(self, line, cell=None):
        """
        Multimodal LLM interaction with Jupyter magics
        """
        args = parse_argstring(self.llm, line)  # self.llm is a bound method

        # Parse the prompt to extract any image paths
        if cell is None:
            prompt = " ".join(args.prompt)
        else:
            prompt = cell
        prompt = parse_paths(prompt)
        prompt_text = prompt["text"]
        paths = prompt["paths"]  # TODO implement check or make parser only output local paths

        # Add the text component of prompt to the message list
        self.messages.append(("human", prompt_text))

        # Add the image components of the query if found
        if paths:
            for path in enumerate(paths):
                # first get the image data
                try:
                    with open(path[1], "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode("utf-8")
                    # append image to the list of images
                    self.images.append(image_data)

                    # generate variable name "image_n" and inject it into a message
                    image_variable_name = f"image_{len(self.images)}"
                    image_message = [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{{{image_variable_name}}}"
                            },
                        }
                    ]
                    self.messages.append(("human", image_message))
                except FileNotFoundError:
                    print(f"Error: Could not read image file {path[1]}")
                    pass

                # Add the image message to the message list

        # Create a dict from self.images to pass the image data to langchain
        image_dict = {f"image_{i+1}": image for i, image in enumerate(self.images)}

        # Get the output from the LLM
        response = get_output(messages=self.messages, image_dict=image_dict).final_output

        # Add LLM response to the message list
        if isinstance(response, ConversationalResponse):
            output = response.response
            self.messages.append(("ai", output))
            return Markdown(output)

        elif isinstance(response, Code):
            output = response
            self.messages.append(("ai", output.prefix))
            cell_fill = output.imports + "\n" + output.code
            get_ipython().set_next_input(cell_fill)
            return Markdown(output.prefix)

    @line_cell_magic
    def chat(self, line, cell=None):
        """
        Live chat with LLM
        """
        while True:
            user_input = input("User: ")
            # print(f'User: {user_input}')

            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            self.messages.append(("human", user_input))
            response = get_output(self.messages).final_output

            if isinstance(response, ConversationalResponse):
                output = response.response
                self.messages.append(("ai", output))
                print(f"Assistant: {output}\n")

            elif isinstance(response, Code):
                output = response
                self.messages.append(("ai", output.prefix))
                cell_fill = output.imports + "\n" + output.code
                print(f"Assistant: {output.prefix}")
                get_ipython().set_next_input(cell_fill)
                break


# If testing interactively, it's convenient to %run as a script in Jupyter
if __name__ == "__main__":
    get_ipython().register_magics(DatalabMagics)
