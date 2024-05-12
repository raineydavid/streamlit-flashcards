# utils.py
# Function to create a flashcard
def generate_flashcard(topic):
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
    return {"question": question.strip(), "answer": answer.strip()}
