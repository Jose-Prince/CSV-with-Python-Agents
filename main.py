from dotenv import load_dotenv
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

    intructions = """
        - You are an agent designed to write and execute Python code to answer questions.
        - You have access to a python REPL, which you can use to execute python code.
        - You have qrcode package installed.
        - You have to give always a name, never an id.+
        - If you get an error, debug your code and try again.
        - Only use the output of your code to answer the question.
        - You might know the answer without running any code, but you should still run the code to get the answer.
        - If it does not seem like you can write code to answer the question, just return "I don't know" as teh answer. 
        """

    st.markdown(intructions)

    st.markdown("### Examples: ")
    ejemplos = [
        "Create a python function for adding to numbers", 
        "Sum 5 + 15", 
        "Create a python function for generating a fibonacci series"
    ]

    example = st.selectbox("Select an example:", ejemplos)

    if st.button("Execute example"):
        user_input = example
        try:
            respuesta = call_output_from_agent(user_input)
            st.markdown("### Agent response: ")
            if "output" in respuesta:
                st.code(respuesta["output"], language="python")
            else:
                st.error("Could not get valid output key.")
        except Exception as e:
            st.error(f"Error en el agente: {str(e)}")

    st.markdown("### Chat with Agent")
    input = st.text_input("Write your prompt",placeholder="Enter your prompt here")

    if input:
        with st.spinner("Generating response..."):
            try:
                response = call_output_from_agent(input)
                st.markdown("### Agent Response: ")
                if "output" in response:
                    st.code(response["output"], language="python")
                else:
                    st.error("No se obtuvo una clave de salida válida.") 
            except Exception as e:
                st.error(f"Error en el agente: {str(e)}")
if __name__ == '__main__':
    main()
