import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🫡",
    layout="centered"
)

# Application title
st.title("AI Interview Assistant")
st.caption("It is a platform for interview preparation and learning.")

# API configuration
try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except (KeyError, FileNotFoundError):
    st.error("API Key is missing. Add it in Streamlit Secrets.")
    st.stop()

# Job role selection
role = st.selectbox(
    "JOB TITLE",
    [
        "Software Engineer",
        "Senior Software Engineer",
        "Data Analyst",
        "Prompt Engineer",
        "DevOps Engineer",
        "Other"
    ]
)

if role == "Other":
    role = st.text_input("Enter your job title", " ")

# Model selection
gen_model = st.selectbox(
    "Choose Model",
    [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b"
    ]
)

# Difficulty level
level = st.selectbox(
    "Difficulty Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

# Activity selection
mode = st.radio(
    "Activity",
    [
        "Generate Questions",
        "Generate Code Questions",
        "Evaluate Answer",
        "Improve Answers"
    ]
)

# Generate questions
if mode == "Generate Questions":

    count = st.slider(
        "Number of Questions",
        1, 10, 5
    )

# Generate coding questions
elif mode == "Generate Code Questions":

    topic = st.selectbox(
        "Topics",
        [
            "SQL",
            "AIML",
            "Python",
            "DSA",
            "C++/C",
            "Java",
            "Cyber Security",
            "ML"
        ]
    )

    count = st.slider(
        "Number of Questions",
        1, 10, 5
    )

# Evaluate or improve answers
else:

    question = st.text_area(
        "Enter Interview Question Here"
    )

    answer = st.text_area(
        "Enter Your Answer",
        height=160
    )

# Generate AI response
if st.button("Generate AI Response", type="primary"):

    if not role.strip():
        st.warning("Please enter a valid job title.")

    elif mode in ["Evaluate Answer", "Improve Answers"] and (
        not question.strip() or not answer.strip()
    ):
        st.warning("Please enter a valid question and answer.")

    else:

        # Background information
        background = (
            "Job Role: " + role +
            "\nDifficulty Level: " + level
        )

        # Create task
        if mode == "Generate Questions":

            task = (
                "Generate " + str(count) +
                " frequently asked interview questions. "
                "Include 3 theory and 2 conceptual questions. "
                "Do not give answers. Give hints."
            )

        elif mode == "Generate Code Questions":

            task = (
                "Generate " + str(count) +
                " frequently asked coding questions on " +
                topic +
                ". Questions can be related to this topic."
            )

        elif mode == "Evaluate Answer":

            task = (
                "Question: " + question +
                "\nMy Answer: " + answer +
                "\nEvaluate this answer based on concept, relevance, "
                "communication and length of answer. "
                "Give each rating out of 5 in a list."
            )

        elif mode == "Improve Answers":

            task = (
                "Question: " + question +
                "\nMy Answer: " + answer +
                "\nImprove the answer based on choice of words "
                "and keywords to include. "
                "Do not invent anything about the candidate."
            )

        # Groq AI response
        with st.spinner("Generating your answer..."):

            try:

                response = client.chat.completions.create(
                    model=gen_model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Act as a senior interviewer, "
                                "both HR and technical expert."
                            )
                        },
                        {
                            "role": "user",
                            "content": background + "\n\n" + task
                        }
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )

                # Display response
                st.subheader("AI Interview Response")

                ai_answer = response.choices[0].message.content

                st.write(ai_answer)

                # Download response
                st.download_button(
                    "Download Answer",
                    data=ai_answer,
                    file_name="AI_Interview_Response.txt",
                    mime="text/plain"
                )

            except Exception as e:

                st.error("Something went wrong!")
                st.exception(e)
