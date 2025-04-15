from crewai import Agent
from tools.pdf_reader import read_pdf
from tools.doc_summarizer import summarize_text

ResearcherAgent = Agent(
    role="Researcher",
    goal="Extract and summarize relevant data from technical documents and user inputs",
    backstory=(
        "You're a domain-savvy assistant skilled in reading PDFs, understanding code structure, "
        "and summarizing documents to provide meaningful context for the R&D team."
    ),
    verbose=True,
    allow_delegation=True
)

def perform_research(file_path):
    text = read_pdf(file_path)
    return summarize_text(text)
