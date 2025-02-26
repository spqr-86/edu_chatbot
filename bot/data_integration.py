# bot/data_integration.py
import os
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS


class CoursesData:
    def __init__(self, csv_path="data/courses.csv"):
        self.csv_path = csv_path
        # Загружаем данные из CSV в виде документов
        self.loader = CSVLoader(file_path=self.csv_path)
        self.documents = self.loader.load()
        # Инициализируем embeddings (используем OpenAIEmbeddings, ключ из переменных окружения)
        self.embeddings = OpenAIEmbeddings()
        # Создаем векторное хранилище на основе документов
        self.vector_store = FAISS.from_documents(self.documents, self.embeddings)

    def query_courses(self, query, k=2):
        """
        Выполняет поиск по курсам. Возвращает объединенный текст из k наиболее релевантных документов.
        """
        results = self.vector_store.similarity_search(query, k=k)
        combined_text = "\n".join([doc.page_content for doc in results])
        return combined_text
