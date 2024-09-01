import pandas as pd
import chromadb

class Portfolio:
    def __init__(self,file_path = "app/resources/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        for index, row in self.data.iterrows():
            tech_stack = row['Techstack']
            link = row['Links']

            # Store metadata
            self.collection.add(
                documents=tech_stack,
                metadatas=[{"links": link}],
                ids=[f"id_{index}"]
            )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])