import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

# ── Tool 1: REAL web search via Tavily ───────────────────────────────────────
web_search = TavilySearchResults(
    max_results=3,          # fetch top 3 results
    description=(
        "Rechercher sur internet des informations sur les paradigmes de programmation, "
        "les concepts informatiques, ou toute question technique."
    )
)

# ── Tool 2: Local docs (keep it but make it honest) ──────────────────────────
@tool
def search_local_docs(query: str) -> str:
    """Chercher dans la documentation locale du cours. Utile pour les consignes spécifiques du Master."""
    # Replace this with real file reading later (e.g. load from PDF/txt)
    local_knowledge = {
        "orienté objet": "Le cours Master insiste sur: encapsulation, héritage, polymorphisme. Voir chapitre 3.",
        "fonctionnel": "Le cours Master insiste sur: fonctions pures, immutabilité, récursion. Voir chapitre 5.",
        "impératif": "Le cours Master insiste sur: séquences d'instructions, états mutables. Voir chapitre 1.",
    }
    for key, value in local_knowledge.items():
        if key in query.lower():
            return value
    return "Aucune documentation locale trouvée pour ce sujet. Essayez une recherche web."


# ── Session memory ────────────────────────────────────────────────────────────
session_store: dict = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


# ── Main factory ──────────────────────────────────────────────────────────────
def get_learning_tools(api_key: str):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,
        temperature=0,   # deterministic = more reliable ReAct parsing
    )

    prompt = hub.pull("hwchase17/react")

    # ✅ Now the agent has 2 real tools to choose from
    tools = [web_search, search_local_docs]

    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=6,
    )

    agent_with_history = RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    def chat_with_alfred(user_message: str, session_id: str = "default") -> str:
        response = agent_with_history.invoke(
            {"input": user_message},
            config={"configurable": {"session_id": session_id}},
        )
        return response["output"]

    return chat_with_alfred