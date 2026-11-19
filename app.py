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
st.caption("It is a platform for getting information")

# API configuration
try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except (KeyError, FileNotFoundError):
    st.error("API Key is missing. Add it in Advanced Settings.")
    st.stop()

# Job title
role = st.selectbox(
    "JOB TITLE",
    [
        "software engineer",
        "senior software engineer",
        "data analyst",
        "prompt engineer",
        "DevOps engineer",
        "other"
    ]
)

if role == "other":
    role = st.text_input("Enter your job title", "XXXXXXX")

# Model selection
gen_model = st.selectbox(
    "model",
    [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b"
    ]
)

# Difficulty level
level = st.selectbox(
    "difficult level",
    [
        "beginner",
        "intermediate",
        "advanced"
    ]
)

# Activity selection
mode = st.radio(
    "Activity",
    [
        "generate questions",
        "generate code questions",
        "evaluate answer",
        "improve answers"
    ]
)

# Generate questions
if mode == "generate questions":

    count = st.slider(
        "Number of questions",
        1, 10, 5
    )

# Generate code questions
elif mode == "generate code questions":

    topic = st.selectbox(
        "Topics",
        [
            "SQL",
            "AIML",
            "Python",
            "DSA",
            "c++/c",
            "Java",
            "cyber security",
            "ML"
        ]
    )

    count = st.slider(
        "Number of questions",
        1, 10, 5
    )

# Evaluate or improve answers
else:

    question = st.text_area(
        "Enter interview question here"
    )

    answer = st.text_area(
        "Enter your answer",
        height=160
    )

# Generate AI response
if st.button("Generate AI Response", type="primary"):

    if not role.strip():
        st.warning("Please enter a valid job title.")

    elif mode in ["evaluate answer", "improve answers"] and (
        not question.strip() or not answer.strip()
    ):
        st.warning("Please enter a valid question and answer.")

    else:

        # Background information
        background = (
            "Job role: " + role +
            "\nDifficulty level: " + level
        )

        # Generate task
        if mode == "generate questions":

            task = (
                "Generate " + str(count) +
                " frequently asked interview questions. "
                "Include 3 theory and 2 conceptual questions. "
                "Do not give answers. Give hints."
            )

        elif mode == "generate code questions":

            task = (
                "Generate " + str(count) +
                " frequently asked coding questions on " +
                topic +
                ". Anything can be related to this topic."
            )

        elif mode == "evaluate answer":

            task = (
                "Question: " + question +
                "\nMy Answer: " + answer +
                "\nEvaluate this answer based on concept, relevance, "
                "communication and length of answer. "
                "Give each rating out of 5 in a list."
            )

        elif mode == "improve answers":

            task = (
                "Question: " + question +
                "\nMy Answer: " + answer +
                "\nImprove the answer based on choice of words "
                "and keywords to include. "
                "Do not invent anything about the candidate."
            )

        # Groq API response
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

                # Display output
                output = response.choices[0].message.content

                st.subheader("AI Response")
                st.markdown(output)

                # Download response
                st.download_button(
                    "Download response",
                    output,
                    file_name="Interview_Response.txt",
                    mime="text/plain"
                )

            except Exception as e:

                st.error(
                    f"API connection was unsuccessful: {e}"
                )

                st.info(
                    "Please check your API key and rate limits."
                )

# Footer
st.caption("Powered by Streamlit.io and GitHub using LLM API")
