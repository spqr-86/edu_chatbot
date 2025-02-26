import pandas as pd

class FAQHandler:
    def __init__(self, faq_path="data/faq.csv"):
        self.faq_path = faq_path
        self.faq_data = pd.read_csv(self.faq_path)

    def find_answer(self, user_question):
        user_question = user_question.lower()
        for _, row in self.faq_data.iterrows():
            if row["question"].lower() in user_question:
                return row["answer"]
        return None
