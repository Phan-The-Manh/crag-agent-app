"""
Agent service for executing the LangGraph agent.
"""
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from fastapi import HTTPException

from agent_app.graph.graph_app import app as agent_graph


class AgentService:
    """Service for managing agent execution."""
    
    def __init__(self):
        """Initialize the agent service."""
        self.agent_graph = agent_graph
    
    def run_agent(self, question: str, thread_id: str) -> str:
        """
        Run the agent with a question.
        
        Args:
            question: The user's question
            thread_id: Thread ID for conversation continuity
            
        Returns:
            The agent's answer as a string
            
        Raises:
            HTTPException: If the agent fails to produce an answer
        """
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {
            "messages": [HumanMessage(content=question.strip())],
        }
        
        try:
            # Stream to end and get final state
            final_state = None
            for output in self.agent_graph.stream(inputs, config=config):
                final_state = output
            
            if not final_state:
                raise HTTPException(
                    status_code=500,
                    detail="Agent produced no output"
                )
            
            # Extract the last message (AI response) from the last node's output
            last_output = list(final_state.values())[0]
            messages = last_output.get("messages", [])
            
            if not messages:
                raise HTTPException(
                    status_code=500,
                    detail="Agent produced no response"
                )
            
            answer = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])
            return answer
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Agent error: {str(e)}"
            )
