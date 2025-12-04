"""
CrewAI-based agent implementation with observability.
"""

import logging
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from openinference.instrumentation.crewai import CrewAIInstrumentor

logger = logging.getLogger(__name__)


def create_crew_llm():
    """Create and configure the ChatOpenAI LLM for CrewAI."""
    return ChatOpenAI(
        model="openrouter/z-ai/glm-4.5-air:free",
        temperature=0.2
    )


def create_crew_agent(task_description: str):
    """
    Create and run a CrewAI agent for a specific task.

    Args:
        task_description: Description of the task to perform.

    Returns:
        Result of the agent execution.
    """
    llm = create_crew_llm()

    agent = Agent(
        role="AI Assistant",
        goal="Complete the user's task effectively",
        backstory="You are a helpful AI assistant capable of performing various tasks.",
        llm=llm
    )

    task = Task(
        description=task_description,
        expected_output="A clear and helpful response to the task.",
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task])
    return crew.kickoff()


def run_crew_agent():
    """Run the interactive CrewAI agent."""
    # Instrument CrewAI for observability
    CrewAIInstrumentor().instrument()

    logger.info("Starting CrewAI agent")
    print("AI Agent Assistant! Describe a task for the agent to perform. Type 'exit' or 'quit' to end.")

    while True:
        try:
            user_input = input("Task: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                logger.info("User ended the agent session")
                print("Goodbye!")
                break

            logger.info(f"Processing task: {user_input[:50]}...")
            result = create_crew_agent(user_input)
            print(f"Agent Result: {result}")
            logger.info("Task completed successfully")

        except KeyboardInterrupt:
            logger.info("Agent interrupted by user")
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error during agent execution: {e}")
            print(f"An error occurred: {e}")
            print("Please try again.")