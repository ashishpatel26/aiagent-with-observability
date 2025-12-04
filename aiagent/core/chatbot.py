"""
LangGraph-based chatbot implementation with observability.
"""

import logging
from typing import Annotated
from os import getenv

from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langfuse.langchain import CallbackHandler
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

# Configure logging
logger = logging.getLogger(__name__)


class State(TypedDict):
    """
    State definition for the LangGraph chatbot.

    The 'messages' key holds the conversation history, with the add_messages
    function ensuring new messages are appended rather than overwritten.
    """
    messages: Annotated[list, add_messages]


def create_chatbot_llm():
    """Create and configure the ChatOpenAI LLM for the chatbot."""
    headers = {}
    if getenv("YOUR_SITE_URL"):
        headers["HTTP-Referer"] = getenv("YOUR_SITE_URL")
    if getenv("YOUR_SITE_NAME"):
        headers["X-Title"] = getenv("YOUR_SITE_NAME")

    return ChatOpenAI(
        api_key=getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        model="z-ai/glm-4.5-air:free",
        temperature=0.2,
        default_headers=headers if headers else None
    )


def create_chatbot_graph():
    """
    Create and configure the LangGraph chatbot.

    Returns:
        Compiled StateGraph ready for execution.
    """
    llm = create_chatbot_llm()

    def chatbot(state: State):
        """
        Chatbot node that processes the current state and generates a response.

        Args:
            state: Current conversation state containing messages.

        Returns:
            Updated state with the AI's response added to messages.
        """
        return {"messages": [llm.invoke(state["messages"])]}

    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.set_entry_point("chatbot")
    graph_builder.set_finish_point("chatbot")

    return graph_builder.compile()


def run_chatbot():
    """Run the interactive chatbot."""
    graph = create_chatbot_graph()
    langfuse_handler = CallbackHandler()

    messages = []
    logger.info("Starting AI agent chatbot")
    print("Chat with the AI agent! Type 'exit' or 'quit' to end.")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                logger.info("User ended the chat session")
                print("Goodbye!")
                break

            messages.append(HumanMessage(content=user_input))
            logger.info(f"Processing user message: {user_input[:50]}...")

            # Stream the response
            response_received = False
            for chunk in graph.stream({"messages": messages}, config={"callbacks": [langfuse_handler]}):
                if 'chatbot' in chunk:
                    ai_message = chunk['chatbot']['messages'][-1]
                    print(f"AI: {ai_message.content}")
                    messages.append(ai_message)
                    response_received = True
                    logger.info("AI response generated successfully")
                    break

            if not response_received:
                logger.warning("No response received from AI")
                print("AI: Sorry, I couldn't generate a response.")

        except KeyboardInterrupt:
            logger.info("Chat interrupted by user")
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error during chat: {e}")
            print(f"An error occurred: {e}")
            print("Please try again.")