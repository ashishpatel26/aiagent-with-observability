import logging
from dotenv import load_dotenv
from typing import Annotated
from os import getenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langfuse.langchain import CallbackHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize Langfuse CallbackHandler for Langchain (tracing)
langfuse_handler = CallbackHandler()

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

headers = {}
if getenv("YOUR_SITE_URL"):
    headers["HTTP-Referer"] = getenv("YOUR_SITE_URL")
if getenv("YOUR_SITE_NAME"):
    headers["X-Title"] = getenv("YOUR_SITE_NAME")

llm = ChatOpenAI(
    api_key=getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="z-ai/glm-4.5-air:free",
    temperature=0.2,
    default_headers=headers if headers else None
)

# The chatbot node function takes the current State as input and returns an updated messages list. This is the basic pattern for all LangGraph node functions.
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Add a "chatbot" node. Nodes represent units of work. They are typically regular python functions.
graph_builder.add_node("chatbot", chatbot)

# Add an entry point. This tells our graph where to start its work each time we run it.
graph_builder.set_entry_point("chatbot")

# Set a finish point. This instructs the graph "any time this node is run, you can exit."
graph_builder.set_finish_point("chatbot")

# To be able to run our graph, call "compile()" on the graph builder. This creates a "CompiledGraph" we can use invoke on our state.
graph = graph_builder.compile()

def main():
    """Main function for the interactive chatbot."""
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
                    break  # Assuming single response per turn

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

if __name__ == "__main__":
    main()