# langchain-qwq

This package contains the LangChain integration with QwQ

## Installation

```bash
pip install -U langchain-qwq
```

And you should configure credentials by setting the following environment variables:

* `DASHSCOPE_API_KEY`: Your DashScope API key for accessing QwQ models
* `DASHSCOPE_API_BASE`: (Optional) API base URL, defaults to "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

## Chat Models

`ChatQwQ` class exposes chat models from QwQ. The integration works directly with a standard API key without requiring the Tongyi dependency.

```python
from langchain_qwq import ChatQwQ

llm = ChatQwQ()
llm.invoke("Sing a ballad of LangChain.")
```

### Advanced Usage

#### Streaming

```python
llm = ChatQwQ(model="qwq-plus")
for chunk in llm.stream("Write a short poem about AI"):
    print(chunk.content, end="")
```

#### Async Support

```python
llm = ChatQwQ(model="qwq-plus")
response = await llm.ainvoke("What is the capital of France?")
print(response.content)

# Streaming
async for chunk in llm.astream("Tell me about quantum computing"):
    print(chunk.content, end="")
```

#### Access to Reasoning Content

```python
response = llm.invoke("Explain how photosynthesis works")
content = response.content
reasoning = response.additional_kwargs.get("reasoning_content", "")
```

#### Tool Calls

```python
from langchain_core.tools import tool

@tool
def get_current_weather(location: str, unit: str = "fahrenheit"):
    """Get the current weather in a given location"""
    return f"72 degrees and sunny in {location}"

llm = ChatQwQ(model="qwq-plus")
llm_with_tools = llm.bind_tools([get_current_weather])
response = llm_with_tools.invoke("What's the weather in San Francisco?")
```
