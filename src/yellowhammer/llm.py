from pydantic import BaseModel, Field
from typing import Union
# from langchain_core.prompts import ChatPromptTemplate
# from .prompt import SYSTEM_PROMPT


# Pydantic schemas to use with .with_structured_output()
# Docstring acts as a description for the LLM
class Code(BaseModel):
    """Schema for code solutions"""

    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")


class ConversationalResponse(BaseModel):
    """Respond in a conversational manner. Be kind and helpful."""

    response: str = Field(description="A conversational response to the user's query")


class FinalResponse(BaseModel):
    """
    Make sure that the final_output field exists.
    final_output can contain either Code or ConversationalResponse schemas.
    """

    final_output: Union[Code, ConversationalResponse]


# Check for errors in the structured output
def error_parser(output):
    """
    Parse the API output to handle errors gracefully.
    """
    if output["parsing_error"]:
        raw_output = str(output["raw"].content)
        error = output["parsing_error"]
        out_string = f"Error parsing LLM output. Parse error: {error}. \n Raw output: {raw_output}"
        return FinalResponse(final_output=ConversationalResponse(response=out_string))

    elif not output["parsed"]:
        raw_output = str(output["raw"].content)
        out_string = f"Error in LLM response. \n Raw output: {raw_output}"
        return FinalResponse(final_output=ConversationalResponse(response=out_string))

    else:
        # Return the parsed output (should be FinalResponse)
        return output["parsed"]


def error_parser(output):
    """
    Parse the API output to handle errors gracefully.
    """
    if output["parsing_error"]:
        raw_output = str(output["raw"].content)
        error = output["parsing_error"]
        out_string = f"Error parsing LLM output. Parse error: {error}. \n Raw output: {raw_output}"
        return FinalResponse(final_output=ConversationalResponse(response=out_string))

    elif not output["parsed"]:
        raw_output = str(output["raw"].content)
        out_string = f"Error in LLM response. \n Raw output: {raw_output}"
        return FinalResponse(final_output=ConversationalResponse(response=out_string))

    else:
        # Return the parsed output (should be FinalResponse)
        return output["parsed"]


def get_chain(
    messages,  # ChatPromptTemplate
    api_provider,
    api_key,
    api_model=None,
    api_temperature=0,
):
    """
    Return a runnable chain which accepts {context} (e.g. datalab API documentation)

    Args:
        messages (ChatPromptTemplate): A ChatPromptTemplate instance
        api_provider (str): API provider name (e.g. "openai", "anthropic")
        api_key (str): LLM API key to use
        api_model (str, optional): The specific model to use e.g. "gpt-4o-mini"
        api_temperature (int, optional): LLM temperature
    """

    # API provider logic
    if api_provider.lower() == "openai":
        from langchain_openai import ChatOpenAI

        if api_model is None:
            api_model = "gpt-4o-mini"
        llm = ChatOpenAI(model=api_model, temperature=api_temperature, openai_api_key=api_key)

    elif api_provider.lower() == "anthropic":
        from langchain_anthropic import ChatAnthropic

        if api_model is None:
            # api_model = "claude-3-5-sonnet-20240620"
            # https://docs.anthropic.com/en/docs/about-claude/models#model-names
            api_model = "claude-3-5-sonnet-latest"
        llm = ChatAnthropic(
            model=api_model,
            temperature=api_temperature,
            anthropic_api_key=api_key,
        )

    # Create a chain where the final output takes the FinalResponse schema
    chain = messages | llm.with_structured_output(FinalResponse, include_raw=True) | error_parser

    return chain
