import os
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Directory to store PDFs
PDF_FOLDER = "./research_papers"
os.makedirs(PDF_FOLDER, exist_ok=True)

def search_arxiv(query, max_results=10):
    """Searches ArXiv for research papers based on the given query."""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print("⚠️ Error fetching data from ArXiv.")
        return []
    
    root = ET.fromstring(response.text)
    papers = []
    
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
        pdf_link = entry.find("{http://www.w3.org/2005/Atom}id").text.strip().replace("abs", "pdf") + ".pdf"
        papers.append({"title": title, "pdf_url": pdf_link})
    
    return papers

def download_pdf(pdf_url, save_folder=PDF_FOLDER):
    """Downloads a PDF from the given URL and saves it to the specified folder."""
    filename = pdf_url.split("/")[-1]
    save_path = os.path.join(save_folder, filename)
    
    response = requests.get(pdf_url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"✅ Downloaded: {filename}")
        return save_path
    else:
        print(f"⚠️ Failed to download: {pdf_url}")
        return None

def fetch_and_download_papers(query, max_results=5):
    """Fetch papers based on a query and automatically download them."""
    papers = search_arxiv(query, max_results)

    if not papers:
        print("No papers found.")
        return []

    print("\n📄 Available Papers:")
    for i, paper in enumerate(papers, 1):
        print(f"{i}. {paper['title']}\n   📄 {paper['pdf_url']}\n")

    downloaded_pdfs = []
    for paper in papers:
        pdf_path = download_pdf(paper["pdf_url"])
        if pdf_path:
            downloaded_pdfs.append(pdf_path)

    return downloaded_pdfs
