from openai import OpenAI
import streamlit as st
from utils import *


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Flashcards Chat")
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for generating a new flashcard
topic = st.text_input("Enter a topic to generate a flashcard:")
if topic:
      stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        prompt=f"Generate a flashcard about: {topic}",
        max_tokens=150,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )
    response = next(stream)['message']['content']
    question, answer = response.text.split(';')  # Assuming the model returns 'question;answer'
    flashcard = {"question": question.strip(), "answer": answer.strip()}
    # flashcard = generate_flashcard(topic)
    st.session_state.flashcards.append(flashcard)

# Displaying flashcards
for flashcard in st.session_state.flashcards:
    with st.expander(f"Flashcard: {flashcard['question']}"):
        st.write("Click to see the answer")
        if st.button("Show Answer", key=flashcard['question']):
            st.write(flashcard['answer'])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = next(stream)['message']['content']
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
