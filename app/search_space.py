# app/search_space.py
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .models import SearchTargetCreate, MatchDocument
from .trusted_search import TrustedAnswerSearch
import uuid

class SearchSpaceManager:
    def __init__(self):
        self.trusted_search = TrustedAnswerSearch()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800, chunk_overlap=100
        )

    def load_pdfs_to_targets(self, pdf_folder: str = "data/docs"):
        """Carrega PDFs e cria targets automaticamente"""
        import os
        created = 0
        
        for filename in os.listdir(pdf_folder):
            if filename.endswith(".pdf"):
                path = os.path.join(pdf_folder, filename)
                loader = PyPDFLoader(path)
                docs = loader.load()
                
                for i, doc in enumerate(docs):
                    chunks = self.text_splitter.split_text(doc.page_content)
                    for j, chunk in enumerate(chunks[:3]):  # limita chunks por página
                        target = SearchTargetCreate(
                            target_id=f"{filename.replace('.pdf','')}-{i}-{j}",
                            description=chunk[:300] + "...",  # descrição curta
                            alternative_phrases=[],
                            match_document=MatchDocument(
                                type="section",
                                title=filename,
                                url=f"/docs/{filename}#page={i+1}",
                                content_summary=chunk[:200]
                            )
                        )
                        self.trusted_search.add_target(target)
                        created += 1
        print(f"✅ {created} targets criados a partir dos PDFs.")
        return created

    def add_manual_target(self, target: SearchTargetCreate):
        self.trusted_search.add_target(target)
        print(f"✅ Target manual adicionado: {target.target_id}")