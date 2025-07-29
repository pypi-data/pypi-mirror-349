"""
Gradio interface for the D4D (Datasheets for Datasets) agent.
"""
from typing import List, Optional

import gradio as gr

from .d4d_agent import d4d_agent
from .d4d_config import D4DConfig, get_config


async def process_url(url: str, history: List[str], config: D4DConfig) -> str:
    """
    Process a URL and generate metadata in YAML format.
    
    Args:
        url: The URL to process (webpage or PDF)
        history: Conversation history
        config: The agent configuration
        
    Returns:
        YAML formatted metadata
    """
    # Run the agent with the URL
    result = await d4d_agent.run(url, deps=config)
    return result.data


def chat(deps: Optional[D4DConfig] = None, **kwargs):
    """
    Create a Gradio chat interface for the D4D agent.
    
    Args:
        deps: Optional dependencies configuration
        kwargs: Additional keyword arguments for configuration
        
    Returns:
        A Gradio ChatInterface
    """
    # Initialize dependencies if needed
    if deps is None:
        deps = get_config(**kwargs)
    
    def get_info(url: str, history: List[str]) -> str:
        """Wrapper for the async process_url function."""
        import asyncio
        return asyncio.run(process_url(url, history, deps))
    
    return gr.ChatInterface(
        fn=get_info,
        type="messages",
        title="Datasheets for Datasets Agent",
        description="Enter a URL to a webpage or PDF describing a dataset. The agent will generate metadata in YAML format according to the complete datasheets for datasets schema.",
        examples=[
            "https://fairhub.io/datasets/2",
            "https://data.chhs.ca.gov/dataset/99bc1fea-c55c-4377-bad8-f00832fd195d/resource/5a6d5fe9-36e6-4aca-ba4c-bf6edc682cf5/download/hci_crime_752-narrative_examples-10-30-15-ada.pdf"
        ]
    )