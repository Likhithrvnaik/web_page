import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Interview",
    page_icon="🤖",
    layout="centered"
)

# Application title
st.title("🤖 AI Interview")
st.caption("Practice and Prepare for your Placement")

st.write("Welcome to your AI Interview Assistant.")

# Import Groq safely
try:
    from groq import Groq
except ImportError:
    st.error("Groq package is not installed.")
    st.info("Install it using: pip install groq")
    st.stop()

# API configuration
try:
    api_key = st.secrets["GROQ_API_KEY"]

    if not api_key:
        st.error("Please add your Groq API key.")
        st.stop()

    client = Groq(api_key=api_key)

except Exception:
    st.error("API key is missing. Add it in Streamlit Secrets.")
    st.stop()

st.success("Groq API connected successfully!")

# Job title selection
role = st.selectbox(
    "Job Title",
    [
        "Machine Learning Engineer",
        "Senior Software Engineer",
        "Data Analyst",
        "Cyber Security",
        "Software Developer",
        "Others"
    ]
)

if role == "Others":
    role = st.text_input("Enter your Job Title")

# Model selection
model = st.selectbox(
    "Choose your model",
    [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b"
    ]
)

# Difficulty level
level = st.selectbox(
    "Choose your level",
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
        "Evaluate Answers",
        "Improve Answers"
    ]
)

# Generate interview questions
if mode == "Generate Questions":

    count = st.slider(
        "Number of Questions",
        1, 10, 5
    )

# Generate coding questions
elif mode == "Generate Code Questions":

    topic = st.selectbox(
        "Select Topic",
        [
            "Python",
            "C++",
            "C",
            "DSA",
            "Aptitude",
            "Java"
        ]
    )

    count = st.slider(
        "Number of Questions",
        1, 10, 5
    )

# Evaluate and improve answers
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

        st.warning("Please enter a valid Job Title.")

    elif mode in ["Evaluate Answers", "Improve Answers"] and (
        not question.strip() or not answer.strip()
    ):

        st.warning("Please enter a valid Question and Answer.")

    else:

        topics = (
            "Job Role: " + role +
            "\nDifficulty: " + level
        )

        # Create task
        if mode == "Generate Questions":

            task = (
                f"Generate {count} frequently asked interview questions "
                f"for the role {role}. Include theory and "
                "situation-based questions with answers."
            )

        elif mode == "Generate Code Questions":

            task = (
                f"Generate {count} frequently asked coding or technical "
                f"questions for the topic {topic}. "
                "Give hints, explanations and accurate answers."
            )

        elif mode == "Evaluate Answers":

            task = (
                f"Question: {question}\n"
                f"Answer: {answer}\n"
                "Evaluate my answer based on the question. "
                "Identify mistakes, explain drawbacks and "
                "give a score out of 10."
            )

        elif mode == "Improve Answers":

            task = (
                f"Question: {question}\n"
                f"Answer: {answer}\n"
                "Improve my answer. Give a professional interview-ready "
                "answer and highlight important points."
            )

        # Connect with Groq AI
        try:

            with st.spinner("AI is generating your response..."):

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an expert AI Interview Assistant. "
                                "Provide accurate, clear and beginner-friendly "
                                "answers for interview preparation."
                            )
                        },
                        {
                            "role": "user",
                            "content": topics + "\n\n" + task
                        }
                    ],
                    temperature=0.7
                )

                # Display response
                st.subheader("AI Interview Response")

                ai_response = response.choices[0].message.content

                st.write(ai_response)

                # Download response
                st.download_button(
                    label="Download AI Response",
                    data=ai_response,
                    file_name="interview_response.txt",
                    mime="text/plain"
                )

        except Exception as e:

            st.error("Error generating AI response.")
            st.exception(e)
