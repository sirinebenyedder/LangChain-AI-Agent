import gradio as gr
from tools.pedagogy import get_learning_tools

def launch_app(api_key):
    # On récupère maintenant une seule fonction de chat
    chat_fn = get_learning_tools(api_key)

    # Fonction wrapper pour adapter Gradio Chat à LangChain
    def respond(message, history):
        # La mémoire est gérée par LangChain en interne via session_id
        return chat_fn(message)

    # Interface de Chat simplifiée
    demo = gr.ChatInterface(
        fn=respond,
        title="🤖 ParaMaster: Paradigms Expert",
        description="Welcome! I am your dedicated AI agent for **Programming Paradigms**. ",
        #"Bienvenue ! Je suis votre tuteur dédié aux **Paradigmes de Programmation. ",
        examples=["Explain the concept of immutability in Functional Programming.",
            "Generate an OOP exercise about inheritance in Python."],
         #["Explique-moi le concept d'immutabilité en programmation fonctionnelle.",
        #  "Génère un exercice de POO sur l'héritage en Python."],
        theme="soft"
    )

    demo.launch(share=True, debug=True)
