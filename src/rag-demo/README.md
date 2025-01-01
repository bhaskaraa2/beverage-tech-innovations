# RAG Demo

A demonstration tool for querying data using Pandas DataFrame and RAG (Retrieval-Augmented Generation) capabilities using LlamaIndex and Ollama.

## Requirements
- Python 3.12
- GPU with minimum 8GB memory
- Hugging Face embeddings
- Ollama LLM

## Installation

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Features

### 1. Pandas DataFrame Queries
Query sales and inventory data through Pandas DataFrame:

```bash
# Check sales for specific store
python src/main.py --action sales --store STORE006 --days 10

# Check inventory for specific store
python src/main.py --action inventory --store STORE006
```

### 2. RAG Query System
Demonstrate document indexing and querying using LlamaIndex:

```bash
python src/main.py --action query
# Example query: "what is store_id"
```

### 3. LangChain Agents
Test LangChain agents using Jupyter Notebook:

```bash
cd src
jupyter notebook
```

## Limitations
- Tool invocation using llama3-groq-tool-use with Ollama is currently not functioning as expected
- Possible compatibility issues between Ollama and LLM model recognition
- Consider using OpenAI or other cloud providers as alternatives for tool integration

## Future Improvements

### LangChain Enhancements
- Implement support for multiple agents
- Add multi-user functionality
- Explore different models and approaches
- Expand tool integration capabilities

### LlamaIndex Improvements
- Integrate vector databases
- Expand unit testing coverage for various scenarios
- Enhance document indexing capabilities

## Documentation References

- [LlamaIndex Documentation](https://docs.llamaindex.ai/en/stable/)
- [LlamaIndex Local Starter Example](https://docs.llamaindex.ai/en/stable/getting_started/starter_example_local/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
