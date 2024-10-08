'''
Author: Aditya Bhatt
Date: 31/08/2024 7:27 AM

TODO: Write code to load data from a PDF

NOTE:
1. This code is designed to load a PDF file, split it into individual pages, and then create an index
   to efficiently search for relevant content using AI-generated embeddings.
2. The FAISS index is used to store and search through high-dimensional embeddings (vector representations) 
   of the PDF's content.
3. Environment variables are used to securely store API keys needed for accessing Google's AI models.
4. Document Embeddings:

When you load the PDF and split it into pages, each page's content is converted into an embedding using Google’s AI model.
Building the Index:

These embeddings are added to the FAISS index, which organizes them for quick similarity search.
Querying the Index:

When you ask a question (like "What is Chain of Thought Prompting?"), the query is converted into an embedding, and FAISS compares it to the embeddings in the index to find the most similar ones.
Returning Results:

The code retrieves the top 2 most similar pages to the query and prints them.
'''

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

# Load environment variables from the .env file to access sensitive information like API keys
load_dotenv()

# Get the current script's directory to handle file paths dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the .env file located in the parent directory of the current script
dotenv_path = os.path.join(os.path.dirname(current_dir), '.env')

# Set the GOOGLE_API_KEY environment variable with the value retrieved from the .env file
# This API key is necessary for accessing Google's AI models to generate embeddings
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Define the path to the PDF file that we want to process
file_path = "../Data/Raw/Prompt-Eng.pdf"

# Initialize the PyPDFLoader with the specified PDF file path
# This loader will read the PDF and allow us to work with its content
loader = PyPDFLoader(file_path)

# Load the PDF content and split it into individual pages
# Each page will be treated as a separate document for the purpose of indexing and searching
pages = loader.load_and_split()

# Print the content of the first page to verify that the PDF was loaded correctly
# print(pages[0])

# Create a FAISS index from the document pages using embeddings generated by Google's AI model
# The embeddings capture the meaning of the text in a high-dimensional vector space
# When dealing with large volumes of data, performing a simple linear search 
#(comparing every item one by one) becomes computationally expensive. 
# Creating an index is a way of structuring the data to allow for efficient search operations.
faiss_index = FAISS.from_documents(pages, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

# Perform a similarity search in the FAISS index for the query "What is Chain of Thought Prompting?"
# The index will return the top 2 pages that are most similar to the query based on the embeddings
docs = faiss_index.similarity_search("What is CHAIN-OF-KNOWLEDGE (COK)?", k=2)

# Loop through the search results and print the page number along with a snippet of the content
# This helps us see which parts of the PDF are most relevant to the query
for doc in docs:
    print(str(doc.metadata["page"]) + ":", doc.page_content[:300])
