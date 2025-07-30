# llm-openhands

[![PyPI](https://img.shields.io/pypi/v/llm-openhands.svg)](https://pypi.org/project/llm-openhands/)
[![Changelog](https://img.shields.io/github/v/release/ftnext/llm-openhands?include_prereleases&label=changelog)](https://github.com/ftnext/llm-openhands/releases)
[![Tests](https://github.com/ftnext/llm-openhands/actions/workflows/test.yml/badge.svg)](https://github.com/ftnext/llm-openhands/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ftnext/llm-openhands/blob/main/LICENSE)



## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-openhands
```
## Usage

Here's an example from https://www.all-hands.dev/blog/programmatically-access-coding-agents-with-the-openhands-cloud-api

**prerequisite**: OpenHands Cloud API key  
https://docs.all-hands.dev/modules/usage/cloud/cloud-api#obtaining-an-api-key

```bash
export LLM_OPENHANDS_KEY=your_api_key_here

llm -m openhands "Check for the authentication module to make sure that it follows the coding best practices for this repo." -o repository https://github.com/yourusername/your-repo
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-openhands
```
Then create a new virtual environment and install the dependencies and test dependencies:
```bash
uv sync --extra test
```
To run the tests:
```bash
uv run pytest
```
