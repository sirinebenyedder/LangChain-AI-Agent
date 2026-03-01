from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Dictionnaire global pour stocker l'historique par session
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def get_learning_tools(api_key):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
    
    # Prompt avec historique : On ajoute MessagesPlaceholder pour la mémoire
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are 'ParaMaster', an expert AI agent in programming paradigms (Imperative, OOP, Functional, Logical). "
            "IMPORTANT: Always respond in the SAME language used by the student. "
            "If the student speaks French, respond in French. If they speak English, respond in English. "
            "Your mission: "
            "- Help students master programming paradigms with clear explanations. "
            "- When generating exercises, specify the target paradigm. "
            "- When reviewing code, strictly check if it follows the requested paradigm's rules."
        )),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    
    chain = prompt | llm

    # On enveloppe la chaîne avec la gestion d'historique
    with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    
    def chat_with_alfred(user_message, session_id="default"):
        config = {"configurable": {"session_id": session_id}}
        response = with_history.invoke({"input": user_message}, config=config)
        return response.content
        
    return chat_with_alfred
