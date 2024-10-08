<div align="center">
  
![h5dy6uwcdiam1zo96es](https://github.com/user-attachments/assets/1712b106-9ab9-4ea3-a697-d5b4686d9070)

# yeLLowhaMmer

</div>

A continuation of the [LLM hackathon](https://www.eventbrite.com/e/llm-hackathon-for-applications-in-materials-and-chemistry-tickets-868303598437) project, [*yeLLowhaMMer: A Multi-modal Tool-calling Agent for Accelerated Research Data Management*](https://github.com/bocarsly-group/llm-hackathon-2024).

This repository will explore using the Jupyter AI plugin to provide an agentic interface to [*datalab*](https://github.com/datalab-org/datalab), with the idea of having this as an additional UI that *datalab* users can use to interact with their data, either deployed for their instance, or run locally.

## Initial development tasks

- [ ] Reproduce the hackathon project with the Jupyter AI plugin, probably by extending the `%%ai` cell magic to something like `%%yellowhammer` that includes the yellowhammer system prompt, and guides through the registration of a *datalab* API key and any provided LLM API keys.
- [ ] Use yellowhammer to generate API examples for the underlying [*datalab-python-api*](https://github.com/datalab-org/datalab-python-api) package.
- [ ] Consider deploying this as a JupyterHub that *datalab* instances can link to directly.
- [ ] Integrate the results much more closely into *datalab* itself, i.e., attaching notebooks to the relevant samples, and recording the provenance of AI generated data recording.

## Installation

This repository uses [`uv`](https://docs.astral.sh/uv/) for the entire packaging workflow.
Once you have installed `uv` following their documentation, you can install this repository by cloning and running `uv sync` in the root directory (optionally with `--dev` if you plan to develop it further).

```shell
git clone git@github.com:datalab-org/yellowhammer
cd yellowhammer
uv sync --dev
```

### Launching example notebooks

You can launch the example notebook locally with `uv` too:

```shell
uv run jupyter lab examples/
```

The examples will require you to bring your own *datalab* API key (for your instance of choice) and API keys for any underlying LLM providers (OpenAI, Anthropic, etc.).

These can be set in your shell profile, or simply in your shell before launching Jupyter, using:
```bash
export OPENAI_API_KEY=sk-proj...
export ANTHROPIC_API_KEY=sk-ant...
```

`yellowhammer` by default will come preloaded with the relevant OpenAI and Anthropic packages.
You can see how to configure other providers in the [Jupyter AI plugin documentation](https://jupyter-ai.readthedocs.io/en/latest/users/index.html#model-providers).
