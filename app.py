
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="LLM",
    layout="centered"
)

# Application title
st.title("AI Interview")
st.caption("Practice and Prepare for your placement")

# API configuration
try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except (KeyError, FileNotFoundError):
    st.error("API key is missing. Add it in Streamlit Secrets.")
    st.stop()

st.success("Groq API connected successfully!")

st.write("Welcome to your AI Interview Assistant.")

# Job role
role = st.selectbox(
    "Job Title",
    [
        "Machine Learning Engineer",
        "Senior Software Engineering",
        "Data Analysis",
        "Cyber Security",
        "Software Developer",
        "Others"
    ]
)

if role == "Others":
    role = st.text_input("Enter your Job Title", "")

# Model selection
model = st.selectbox(
    "Choose your model",
    [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b"
    ]
)

# Experience level
level = st.selectbox(
    "Choose your level",
    ["Beginner", "Intermediate", "Advanced"]
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

# Input based on activity
if mode == "Generate Questions":

    count = st.slider("Number of Questions", 1, 10, 5)

elif mode == "Generate Code Questions":

    topic = st.selectbox(
        "Select Topic",
        ["Python", "C++", "C", "DSA", "Aptitude", "Java"]
    )

    count = st.slider("Number of Questions", 1, 10, 5)

else:

    question = st.text_area("Enter Interview Question Here")

    answer = st.text_area(
        "Enter Your Answer",
        height=160
    )

# Generate AI response
if st.button("Generate AI Response", type="primary"):

    if not role.strip():
        st.warning("Please enter a valid job title.")
        st.stop()

    # Generate prompt
    if mode == "Generate Questions":

        prompt = f"""
        Generate {count} interview questions for the role
        of {role}.

        Experience Level: {level}

        Provide clear and relevant interview questions.
        """

    elif mode == "Generate Code Questions":

        prompt = f"""
        Generate {count} coding interview questions.

        Job Role: {role}
        Topic: {topic}
        Experience Level: {level}

        Include coding problems and expected difficulty.
        """

    elif mode == "Evaluate Answers":

        if not question.strip() or not answer.strip():
            st.warning("Please enter both question and answer.")
            st.stop()

        prompt = f"""
        Evaluate the following interview answer.

        Job Role: {role}
        Experience Level: {level}

        Question: {question}

        Candidate Answer: {answer}

        Provide:
        1. Score out of 10
        2. Strengths
        3. Weaknesses
        4. Suggestions for improvement
        """

    else:

        if not question.strip() or not answer.strip():
            st.warning("Please enter both question and answer.")
            st.stop()

        prompt = f"""
        Improve the following interview answer.

        Job Role: {role}
        Experience Level: {level}

        Question: {question}

        Original Answer: {answer}

        Provide a professional, clear and technically
        accurate improved answer.
        """

    # Call Groq API
    try:
        with st.spinner("Generating AI response..."):

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert technical interview assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7
            )

            result = response.choices[0].message.content

        st.subheader("AI Interview Response")
        st.markdown(result)

    except Exception as e:
        st.error(f"Something went wrong: {e}")

