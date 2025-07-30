import json
from typing import Dict, Any, List

from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

from limbic.tools.decorator import ToolExecutionError, tool

@tool
def analyze_research(query: str, results: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Analyze research results using an LLM.

    Parameters:
    -----------
    query: str
        The original research query.
    results: List[Dict[str, str]]
        List of research results to analyze.

    Returns:
    --------
    Dict[str, Any]
        Analysis containing key findings, themes, gaps, and recommendations.
    """
    try:
        llm = ChatOpenAI(model_name="gpt-4-turbo-preview")
        
        # Prepare the context from results
        context = "\n\n".join([
            f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['snippet']}"
            for r in results
        ])
        
        # Create the prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a research assistant. Analyze the provided research results and synthesize key findings."),
            HumanMessage(content=f"Research Query: {query}\n\nResearch Results:\n{context}\n\nPlease analyze these results and provide:\n1. Key findings\n2. Common themes\n3. Potential gaps in information\n4. Recommendations for further research")
        ])
        
        # Get analysis from LLM
        response = llm.invoke(prompt)
        return {
            "analysis": response.content,
            "sources": [{"title": r['title'], "url": r['url']} for r in results]
        }
    except Exception as e:
        raise ToolExecutionError(
            message=f"Failed to analyze research results: {str(e)}",
            developer_message=f"Error in analyze_research: {str(e)}"
        )