import streamlit as st
import time
import os

import instructor
from pydantic import BaseModel
from typing import List, Optional
import openai
import enum


class UserDetail(BaseModel):
    name: str
    age: int
    passions: List[str]


def data_extraction_submit(openai_client, input: str, model: str) -> UserDetail:
    client = instructor.patch(client=openai_client)
    user = client.chat.completions.create(
        model=model,
        response_model=UserDetail,
        messages=[
            {"role": "system", "content": "Extract all user information"},
            {"role": "user", "content": input},
        ],
    )
    assert isinstance(user, UserDetail)
    return user


def data_extraction_form(openai_client, model: str):
    with st.form('data-extraction'):
        st.subheader('pydantic model')
        code = '''
        from pydantic import BaseModel
        from typing import List

        class UserDetail(BaseModel):
            name: str
            age: int
            passions: List[str]
        '''
        st.code(code, language="python")


        text = st.text_area('Enter text:',
                            'My name is Jason, I am 25 years old, my passions are the bowling and the rock music.')
        submitted = st.form_submit_button('Submit')
        if submitted:
            user = data_extraction_submit(openai_client, text, model)
            st.info(user)