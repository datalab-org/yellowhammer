from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from .prompt import SYSTEM_PROMPT
from typing import Union


# Pydantic schema to use with .with_structured_output()
class code(BaseModel):
    """Schema for code solutions"""

    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")


class ConversationalResponse(BaseModel):
    """Respond in a conversational manner. Be kind and helpful."""

    response: str = Field(description="A conversational response to the user's query")


class FinalResponse(BaseModel):
    """The final response can be either a code solution or a conversational response"""

    final_output: Union[code, ConversationalResponse]


def get_chain(
    api_provider,
    api_key,
    api_model=None,
    api_temperature=0,
):
    # API provider logic
    if api_provider.lower() == "openai":
        from langchain_openai import ChatOpenAI

        if api_model is None:
            api_model = "gpt-4o-mini"
        llm = ChatOpenAI(model=api_model, temperature=api_temperature, openai_api_key=api_key)

    elif api_provider.lower() == "anthropic":
        from langchain_anthropic import ChatAnthropic

        if api_model is None:
            api_model = "claude-3-5-sonnet-20240620"
        llm = ChatAnthropic(
            model=api_model,
            temperature=api_temperature,
            anthropic_api_key=api_key,
        )

    # Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT,
            ),  # datalab API info is passed via {context} to the system prompt
            ("placeholder", "{messages}"),
        ]
    )

    # Create a chain where the final output takes the FinalResponse schema
    chain = prompt | llm.with_structured_output(FinalResponse, include_raw=False)

    # Returns a runnable chain which accepts datalab API documentation "context" and user question "messages"
    return chain
