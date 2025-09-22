from enum import StrEnum


class HelpSection(StrEnum):
    faq = "faq"
    contact = "contact"
    instructions = "instructions"


class FAQItem:
    def __init__(self, question: str, answer: str, category: str = "general"):
        self.question = question
        self.answer = answer
        self.category = category
