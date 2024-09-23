import streamlit as st
import time
import os

import instructor
from pydantic import BaseModel
from typing import List, Optional
import openai
import enum


# Define Enum class for multiple labels
class MultiLabels(str, enum.Enum):
    AUTHENTICATION = "authentication"
    BILLING = "billing"
    HARDWARE = "hardware"


# Define the multi-class prediction model
class MultiClassPrediction(BaseModel):
    """
    Class for a multi-class label prediction.
    """

    class_labels: List[MultiLabels]


def text_multi_classification_submit(openai_client, input: str, model: str) -> MultiClassPrediction:
    client = instructor.patch(client=openai_client)
    multi_prediction = client.chat.completions.create(
        model=model,
        response_model=MultiClassPrediction,
        messages=[
            {"role": "system", "content": "Classify the user support ticket with the correspond label(s)"},
            {"role": "user", "content": input},
        ],
    )

    assert isinstance(multi_prediction, MultiClassPrediction)
    return multi_prediction

def text_multi_classification_form(openai_client, model: str):
    with st.form('text-multi-classification-form'):
        st.subheader('labels enum')
        code = '''
    import enum
    from pydantic import BaseModel
    from typing import List

    # Define Enum class for multiple labels
    class MultiLabels(str, enum.Enum):
        AUTHENTICATION = "authentication"
        BILLING = "billing"
        HARDWARE = "hardware"
    
    
    # Define the multi-class prediction model
    class MultiClassPrediction(BaseModel):
        """
        Class for a multi-class label prediction.
        """
    
        class_labels: List[MultiLabels]
                '''
        st.code(code, language="python")

        text = st.text_area('Enter text:',
                            'My account is locked and I can\'t access my billing info.')
        submitted = st.form_submit_button('Submit')
        if submitted:
            classification = text_multi_classification_submit(openai_client, text, model)
            st.info(classification)