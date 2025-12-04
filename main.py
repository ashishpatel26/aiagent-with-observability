from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from openinference.instrumentation.crewai import CrewAIInstrumentor

load_dotenv()

# Instrument CrewAI for observability
CrewAIInstrumentor().instrument()

# Initialize LLM
llm = ChatOpenAI(
    model="openrouter/z-ai/glm-4.5-air:free",
    temperature=0.2)

def main():
    print("AI Agent Assistant! Describe a task for the agent to perform. Type 'exit' or 'quit' to end.")
    while True:
        user_input = input("Task: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        # Create agent
        agent = Agent(
            role="AI Assistant",
            goal="Complete the user's task effectively",
            backstory="You are a helpful AI assistant capable of performing various tasks.",
            llm=llm
        )

        # Create task based on user input
        task = Task(
            description=user_input,
            expected_output="A clear and helpful response to the task.",
            agent=agent
        )

        # Create and run crew
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        print(f"Agent Result: {result}")

if __name__ == "__main__":
    main()
