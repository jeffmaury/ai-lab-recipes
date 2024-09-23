
import streamlit as st
import time
import os

import instructor
from pydantic import BaseModel
from typing import List, Optional
import openai
import enum


class Labels(str, enum.Enum):
    """Enumeration for single-label text classification."""
    SPAM = "spam"
    NOT_SPAM = "not_spam"


class SinglePrediction(BaseModel):
    """
    Class for a single class label prediction.
    """

    class_label: Labels


def text_classification_submit(openai_client, input: str, model: str) -> SinglePrediction:
    client = instructor.patch(client=openai_client)
    single_prediction = client.chat.completions.create(
        model=model,
        response_model=SinglePrediction,
        messages=[
            {"role": "system", "content": "Classify the user text"},
            {"role": "user", "content": input},
        ],
    )

    assert isinstance(single_prediction, SinglePrediction)
    return single_prediction


def text_classification_form(openai_client, model: str):
    with st.form('text-classification-form'):
        st.subheader('labels enum')
        code = '''
    import enum
    from pydantic import BaseModel

    class Labels(str, enum.Enum):
        """Enumeration for single-label text classification."""

        SPAM = "spam"
        NOT_SPAM = "not_spam"
    class SinglePrediction(BaseModel):

        """
        Class for a single class label prediction.
        """
        class_label: Labels
                '''
        st.code(code, language="python")

        text = st.text_area('Enter text:',
                            'Hello there I\'m a prince from a far country and I want to give you money. I need you to give me money and I will send you the double')
        submitted = st.form_submit_button('Submit')
        if submitted:
            classification = text_classification_submit(openai_client, text, model)
            st.info(classification)




