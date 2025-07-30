import os
import json

from typing import List

from limbic.tools.decorator import ToolExecutionError, tool
from limbic.utils import get_quotient_logger

logger = get_quotient_logger()

@tool
def web_search(query: str, max_results: int = 5, format: str = "markdown") -> str:
    """
    Search the web for a given query using the Tavily api.

    parameters:
    -----------
    query: str
        the search query to look up.
    max_results: int
        maximum number of results to return (default: 5).
    format: str
        output format, either "json" or "markdown" (default: markdown).

    returns:
    --------
    str
        search results in the specified format.
    """
    try:
        from tavily import TavilyClient
    except ImportError:
        raise ToolExecutionError(
            message="tavily-python not installed. please install using `pip install tavily-python`",
            developer_message="missing dependency: pip install tavily-python"
        )

    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise ToolExecutionError(
            message="tavily api key not found. please set the TAVILY_API_KEY environment variable",
            developer_message="environment variable TAVILY_API_KEY is not set"
        )

    client = TavilyClient(api_key=api_key)
    
    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            include_answer=False,
            max_results=max_results
        )
        # log results to quotient to find hallucinations
        # logger.log(
        #     user_query=query,
        #     model_output=response.get("answer", ""),
        #     documents=[r["content"] for r in response.get("results", [])],
        #     tags={
        #         "tool": "web_search",
        #         "query": query,
        #         "max_results": max_results,
        #         "format": format,
        #     }
        # )
        
        if format == "json":
            clean_response = {
                "query": query,
                "answer": response.get("answer"),
                "results": [{
                    "title": r["title"],
                    "url": r["url"],
                    "content": r["content"],
                    "score": r["score"]
                } for r in response.get("results", [])]
            }
            data = json.dumps(clean_response)
            return data
        else:  # markdown format
            markdown = f"# {query}\n\n"
            if "answer" in response:
                markdown += "### summary\n"
                markdown += f"{response['answer']}\n\n"
            for result in response.get("results", []):
                markdown += f"### [{result['title']}]({result['url']})\n"
                markdown += f"{result['content']}\n\n"
            return markdown
            
    except Exception as e:
        raise ToolExecutionError(
            message="error performing web search",
            developer_message=f"tavily api error: {str(e)}"
        )

@tool
def web_extract(urls: List[str], include_images: bool = False, format: str = "markdown") -> str:
    """
    Extract content from a list of URLs using the Tavily API.

    Parameters:
    -----------
    urls: List[str]
        List of URLs to extract content from.
    include_images: bool
        Whether to include image URLs in the response (default: False).
    format: str
        Output format, either "json" or "markdown" (default: markdown).

    Returns:
    --------
    str
        Extracted content in the specified format.
    """
    try:
        from tavily import TavilyClient
    except ImportError:
        raise ToolExecutionError(
            message="tavily-python not installed. Please install using `pip install tavily-python`",
            developer_message="missing dependency: pip install tavily-python"
        )

    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise ToolExecutionError(
            message="Tavily API key not found. Please set the TAVILY_API_KEY environment variable",
            developer_message="environment variable TAVILY_API_KEY is not set"
        )

    client = TavilyClient(api_key=api_key)
    
    try:
        response = client.extract(
            urls=urls,
            include_images=include_images
        )
        
        # Log results to quotient
        # logger.log(
        #     user_query=f"Extract content from URLs: {', '.join(urls)}",
        #     # No model output for extraction
        #     model_output="",
        #     documents=[r["raw_content"] for r in response.get("results", [])],
        #     tags={
        #         "tool": "web_extract",
        #         "urls": urls,
        #         "include_images": include_images,
        #         "format": format,
        #     }
        # )
        
        if format == "json":
            return json.dumps(response)
        else:  # markdown format
            markdown = "# Extracted Web Content\n\n"
            for result in response.get("results", []):
                markdown += f"## {result['url']}\n\n"
                markdown += f"{result['raw_content']}\n\n"
                if include_images and result.get("images"):
                    markdown += "### Images:\n"
                    for img_url in result["images"]:
                        markdown += f"- {img_url}\n"
                markdown += "---\n\n"
            
            if response.get("failed_results"):
                markdown += "## Failed Extractions\n"
                for failed in response["failed_results"]:
                    markdown += f"- {failed}\n"
            
            return markdown
            
    except Exception as e:
        raise ToolExecutionError(
            message="Error extracting content from URLs",
            developer_message=f"Tavily API error: {str(e)}"
        )
