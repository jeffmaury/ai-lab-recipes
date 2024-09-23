import streamlit as st
import time
import os

import instructor
from pydantic import BaseModel
from typing import List, Optional
import openai
import enum

from data_extraction import data_extraction_form
from multi_text_classification import text_multi_classification_form
from function_calling import function_calling_form
from text_single_classification import text_classification_form

model_service = os.getenv("MODEL_ENDPOINT",
                          "http://localhost:8888")
model_service = f"{model_service}/v1"

st.set_page_config(page_title="Function Calling")
st.title('🧩 Function Calling')

openai_client = openai.OpenAI(
    api_key="dummy",  # can be anything
    base_url=model_service,  # NOTE: Replace with IP address and port of your llama-cpp-python server
)


@st.cache_resource(show_spinner=False)
def checking_model_service() -> List[str]:
    print("Checking Model Service Availability...")
    ready = False
    while not ready:
        try:
            global models
            models = [model.id for model in openai_client.models.list().data]
            return models
        except:
            pass
        time.sleep(1)


def main() -> None:
    models: List[str] = []
    with st.spinner("Checking Model Service Availability..."):
        models = checking_model_service()

    select_model = models[0]

    st.info(f'Using {select_model}')

    data_extraction_tab, text_single_classification_tab, text_multi_classification_tab, function_calling_tab = st.tabs([
        "Data extraction",
        "Text single classification",
        "Text multi classification",
        "Function calling",
    ])

    with data_extraction_tab:
        data_extraction_form(openai_client, select_model)

    with text_single_classification_tab:
        text_classification_form(openai_client, select_model)

    with text_multi_classification_tab:
        text_multi_classification_form(openai_client, select_model)

    with function_calling_tab:
        function_calling_form(openai_client, select_model)


main()
