from typing import Any, Dict
from dotenv import load_dotenv
from langchain import hub
from langchain_core.tools import Tool
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
import streamlit as st
from backend import call_output_from_agent

load_dotenv()

def main():
    st.set_page_config(
        page_title="Movie-Python Agent",
        page_icon="",
        layout="wide"
    )

    st.title("Interactive Movie-Python Agent")
    st.markdown(
        """
        <style>
        .stApp{background-color:black;}
        .title{color=#ff4b4b;}
        .button{background-color: #ff4b4b; color: white;border-radius: 5px;}
        .input{border: 1px solid #ff4b4b; border-radius: 5px;}
        </style>
        """,
        unsafe_allow_html=True
    )

    instrucciones = """
        - Siempre usa la herramienta, incluso si sabes la respuesta.
        - Debes usar código de Python para responder.
        - Eres un agente que puede escribir código.
        - Solo respondes la pregunta escribiendo código se sabes la respuesta.
        - Si no sabes la respuesta escribe "No sé la respuesta".
        """

    st.markdown(instrucciones)

    st.markdown("### Ejemplos: ")
    ejemplos = [
        "Calcula la suma de 2 y 3", 
        "Genera una lista del 1 al 10", 
        "Crea una función que calcule el factorial de un número",
        "Crea un juego básico de snake con la librería pygame"
    ]

    example = st.selectbox("Selecciona un ejemplo:", ejemplos)

    if st.button("Ejecutar ejemplo"):
        user_input = example
        print(user_input)
        try:
            respuesta = call_output_from_agent(user_input)
            st.markdown("### Respuesta del agente: ")
            if "output" in respuesta:
                st.code(respuesta["output"], language="python")
            else:
                st.error("No se obtuvo una clave de salida válida.")
        except Exception as e:
            st.error(f"Error en el agente: {str(e)}")

if __name__ == '__main__':
    main()
