import os
from crewai import Agent, Crew, Process, Task
from crewai_tools import PDFSearchTool
from dotenv import load_dotenv

# Load environment variables (ensure API keys are set in a .env file)
load_dotenv()

# Function to get all PDFs from "research_papers" folder
def get_pdf_tools(pdf_folder="./research_papers"):
    pdf_paths = [os.path.join(pdf_folder, file) for file in os.listdir(pdf_folder) if file.endswith(".pdf")]
    pdf_tools = []
    for pdf_path in pdf_paths:
        try:
            pdf_tool = PDFSearchTool(
                pdf=pdf_path,
                config=dict(
                    llm=dict(provider="groq", config=dict(model="Llama 3.1 70B/8B")),
                    embedder=dict(provider="ollama", config=dict(model="all-minilm")),
                ),
            )
            pdf_tools.append(pdf_tool)
        except Exception as e:
            print(f"Error initializing PDFSearchTool for {pdf_path}: {e}")
    return pdf_tools

# Function to process the query and search in PDFs
def process_query(query):
    pdf_tools = get_pdf_tools()
    if not pdf_tools:
        print("No valid PDFs found or failed to initialize PDF tools.")
        return "No valid PDFs available for search."

    # Create the research agent
    research_agent = Agent(
        role="Research Agent",
        goal="Search through PDFs to find relevant answers",
        allow_delegation=False,
        verbose=True,
        backstory="The research agent specializes in retrieving information from multiple PDFs.",
        tools=pdf_tools,
    )

    # Define the research task
    answer_query_task = Task(
        description=f"""
        Answer the researcher's query based on the provided PDFs.
        The research agent will search through multiple PDFs to find relevant answers.
        Query: {query}
        """,
        expected_output="Provide clear and accurate answers based on the research papers.",
        tools=pdf_tools,
        agent=research_agent,
    )

    # Create a crew
    crew = Crew(
        tasks=[answer_query_task],
        agents=[research_agent],
        process=Process.sequential,
    )

    try:
        return crew.kickoff(inputs={"query": query})
    except Exception as e:
        print(f"Error executing research task: {e}")
        return "An error occurred while processing the query."
