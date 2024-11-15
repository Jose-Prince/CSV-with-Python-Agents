from typing import Any, Dict
from dotenv import load_dotenv
from langchain import hub
from langchain_core.tools import Tool
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool

load_dotenv()

def main():
    print("Start...")

    intructions = """
        You are an agent designed to write and execute Python code to answer questions.
        You have access to a python REPL, which you can use to execute python code.
        You have qrcode package installed.
        You have to give always a name, never an id.+
        If you get an error, debug your code and try again.
        Only use the output of your code to answer the question.
        You might know the answer without running any code, but you should still run the code to get the answer.
        If it does not seem like you can write code to answer the question, just return "I don't know" as teh answer. 
        """

    base_prompt= hub.pull("langchain-ai/react-agent-template")

    tools = [PythonREPLTool()]
    
    prompt = base_prompt.partial(instructions=intructions)

    agent = create_react_agent(
            prompt=prompt,
            llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
            tools=tools,
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    netflix_agent_executor : AgentExecutor = create_csv_agent(
        llm= ChatOpenAI(temperature=0, model='gpt-4'),
        path="netflix_titles.csv",
        verbose=True,
        allow_dangerous_code = True,
    )
    hbo_agent_executor : AgentExecutor = create_csv_agent(
        llm= ChatOpenAI(temperature=0, model='gpt-4'),
        path="data.csv",
        verbose=True,
        allow_dangerous_code = True,
    )
    disney_agent_executor : AgentExecutor = create_csv_agent(
        llm= ChatOpenAI(temperature=0, model='gpt-4'),
        path="disney_plus_titles.csv",
        verbose=True,
        allow_dangerous_code = True,
    )
    primev_agent_executor : AgentExecutor = create_csv_agent(
        llm= ChatOpenAI(temperature=0, model='gpt-4'),
        path="amazon_prime_titles.csv",
        verbose=True,
        allow_dangerous_code = True,
    )

    def python_agent_executor_wrapper(original_prompt: str) -> dict[str,Any]:
        return agent_executor.invoke({"input": original_prompt})
    
    tools = [
        Tool(
            name="Python Agent",
            func=python_agent_executor_wrapper,
            description="""useful when you need to transform natural language to python and execute the python code,
            returning the results of the code execution
            DOES NOT ACCEPT CODE AS INPUT""",
        ),
        Tool(
            name="Prime_Video Agent",
            func=primev_agent_executor.invoke,
            description="""useful when you need to answer questions related to Prime Video series and movies in amazon_prime_titles.csv file,
            takes as an input the entire question and returns the answer after running pandas calculation
            """,
        ),
        Tool(
            name="Disney+ Agent",
            func=disney_agent_executor.invoke,
            description="""useful when you need to answer questions related to Disney+ series and movies in disney_plus_titles.csv file,
            takes as an input the entire question and returns the answer after running pandas calculation
            """,
        ),
        Tool(
            name="Max Agent",
            func=hbo_agent_executor.invoke,
            description="""useful when you need to answer questions related to Max series and movies in data.csv file,
            takes as an input the entire question and returns the answer after running pandas calculation
            """,
        ),
        Tool(
            name="Netflix Agent",
            func=netflix_agent_executor.invoke,
            description="""useful when you need to answer questions related to Netflix series and movies in netflix_titles.csv file,
            takes as an input the entire question and returns the answer after running pandas calculation
            """,
        ),
    ]

    grand_agent=create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        tools=tools,
    )

    grand_agent_executor = AgentExecutor(
        agent=grand_agent,
        tools=tools,
        verbose=True,
    )

    print(
        grand_agent_executor.invoke(
            {
                "input": "Give me a function for obtainig factorial for a number"
            }
        )
    )

if __name__ == '__main__':
    main()
