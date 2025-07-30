from .llmpy import LLM, Model

_llm = LLM()

def ask(model, question):
    return _llm.ask(model, question)


def ask_many(models, question):
    return _llm.ask_many(models, question)