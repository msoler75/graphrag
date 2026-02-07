#!/usr/bin/env python3
"""
Test script for GraphRAG indexing with Ollama.
This script demonstrates how to use GraphRAG with Ollama as the LLM provider.
"""

import os
import asyncio
from pathlib import Path

from graphrag.config.models.graph_rag_config import GraphRagConfig
from graphrag.api import build_index


async def main():
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Create sample input data
    input_dir = Path("input")
    input_dir.mkdir(exist_ok=True)

    # Sample configuration for Ollama
    # Note: Make sure Ollama is running locally and the model is pulled
    config = GraphRagConfig(**{
        "root_dir": str(output_dir),
        "input": {
            "type": "text",
            "file_type": "text",
            "base_dir": str(input_dir),
            "file_pattern": ".*\\.txt$",
        },
        "storage": {
            "type": "file",
            "base_dir": str(output_dir / "storage"),
        },
        "reporting": {
            "type": "file",
            "base_dir": str(output_dir / "reports"),
        },
        "cache": {
            "type": "json",
            "base_dir": str(output_dir / "cache"),
        },
        "vector_store": {
            "type": "lancedb",
            "db_uri": str(output_dir / "lancedb" / "lancedb.sqlite"),
            "container_name": "default",
            "overwrite": True,
        },
        "completion_models": {
            "default_completion_model": {
                "type": "litellm",
                "model_provider": "ollama",
                "model": "llama3.2:3b",
                "api_base": "http://localhost:11434",
                "api_key": "dummy",
                "max_tokens": 4096,
                "max_retries": 3,
                "max_retry_wait": 10.0,
                "model_kwargs": {
                    "temperature": 0.0,
                    "top_p": 1.0,
                }
            }
        },
        "embedding_models": {
            "default_embedding_model": {
                "type": "litellm",
                "model_provider": "ollama",
                "model": "nomic-embed-text",
                "api_base": "http://localhost:11434",
                "api_key": "dummy",
                "max_tokens": 8192,
                "max_retries": 3,
                "max_retry_wait": 10.0,
            }
        },
        "parallelization": {
            "stagger": 0.3,
            "num_threads": 4,
        },
        "async_mode": "asyncio",
        "entity_extraction": {
            "entity_types": ["organization", "person", "geo", "event"],
            "max_gleanings": 1,
        },
        "summarize_descriptions": {
            "max_length": 500,
        },
        "community_reports": {
            "max_length": 2000,
            "max_input_length": 8000,
        },
    })

    sample_text = """
    GraphRAG is a powerful tool for analyzing text data using graph-based methods.
    It combines large language models with graph algorithms to extract insights from documents.

    Microsoft developed GraphRAG to help researchers and analysts understand complex datasets.
    The system can identify entities, relationships, and communities within text corpora.

    Key features include:
    - Entity extraction from unstructured text
    - Relationship identification between entities
    - Community detection in knowledge graphs
    - Global and local search capabilities

    GraphRAG supports various LLM providers including OpenAI, Azure OpenAI, and local models via Ollama.
    This makes it flexible for different deployment scenarios and cost considerations.
    """

    with open(input_dir / "sample.txt", "w") as f:
        f.write(sample_text)

    print("Starting GraphRAG indexing with Ollama...")

    # Run the indexing pipeline
    results = await build_index(config=config)
    
    print(f"Indexing completed with {len(results)} pipeline runs!")
    print(f"Output saved to: {output_dir}")


if __name__ == "__main__":
    asyncio.run(main())