import os
from dotenv import load_dotenv


from llama_index.llms.openai import OpenAI
from prompt import data_visualization_prompt


import pandas as pd
import base64
from io import BytesIO
import plotly.express as px

# Load environment variables from .env file
load_dotenv()
llm = OpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)


def execute_function(function_string: str, dataframe: pd.DataFrame) -> str:
    # Define the function dynamically
    exec(function_string, globals())

    # Call the function with the dataframe
    figure = visualize_data(dataframe)

    # Convert the plotly figure to HTML for display
    # Convert the plotly figure to base64 image

    buffer = BytesIO()
    figure.write_image(buffer, format="png")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    print("Generated image for the plot.")
    return f"data:image/png;base64,{img_str}"


def data_visualization_agent(csv_file_path: str, user_query: str) -> str:
    dataframe = pd.read_csv(csv_file_path)
    prompt_to_llm = (
        data_visualization_prompt
        + "\n\nDataset"
        + dataframe.to_string()
        + "\n\nUser Query: "
        + user_query
    )
    response = llm.complete(prompt_to_llm)
    function_string = response.text.strip("```python")

    return execute_function(function_string, dataframe)
