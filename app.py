import gradio as gr
from tools.pedagogy import get_learning_tools

def launch_app(api_key):
    chat_fn = get_learning_tools(api_key)

    #Wrapper fonction
    def respond(message, history):
        return chat_fn(message)

    # Chat UI
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
