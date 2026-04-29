import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

#Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Primary model - Gemma 4 for hackathon
try:
    model = genai.GenerativeModel("models/gemma-4-26b-a4b-it")
except Exception:
    # Backup model if primary is not available
    model = genai.GenerativeModel("models/gemma-3-12-it")

#Page configuration
st.set_page_config(page_title="Vidya AI", page_icon="🎓", layout="wide")

# Custom CSS for better look
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .header {
            text-align: center;
            padding: 20px;
            background-color: #4a90e2;
            color: white;
            border-radius: 10px;
        }
        .input-area {
            margin-top: 30px;
        }
        .output-area {
            margin-top: 30px;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)  

#Header
st.title("🎓 Vidya AI")
st.subheader("Empowerng Every student- Anytime, Anywhere")
st.markdown("---")

#Side bar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
st.sidebar.title("Vidya AI")
st.sidebar.markdown("Your Personal AI Tutor")
st.sidebar.markdown("---")

#Language selection
language = st.sidebar.selectbox("Select Language", ["English", "Hindi"]) 

#Feature selection
feature = st.sidebar.radio(
       "Select Feature", 
        ["💭Ask VIDYA", 
         "📚NCERT Helper", 
         "📄Exam Preparation", 
         "🧑‍🏫Teacher Assistance",
         "📊Performance Tracker"]) 

st.sidebar.markdown("---")
st.sidebar.markdown("Built for Gemma 4 Good Hackathon 2026")
st.sidebar.markdown("By Bharat Sharma")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Helper function for language
def get_language_prompt(language):
    if language == "Hindi":
        return "Answer in simple Hindi language that a rural Indian student can understand."
    return "Answer in simple English that a rural Indian student can understand."

# Feature 1 - Ask VIDYA
if feature == "💭Ask VIDYA":
    st.header("💭 Ask VIDYA Anything")
    if language == "Hindi":
        st.markdown("VIDYA से कोई भी सवाल पूछें, चाहे वो गणित हो, विज्ञान हो या सामान्य ज्ञान।")
    else:
        st.write("Your personal AI teacher - available 24/7, even offline")
        
    #Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    #User input
    if language == "Hindi":
        placeholder ="अपना सवाल यहाँ लिखें..."
    else:
        placeholder ="Ask your stdy question here..."
        
    if prompt := st.chat_input(placeholder):
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                full_prompt = f"""You are VIDYA, an AI tutor designed to help rural Indian students with their studies. {get_language_prompt(language)} Use simple words, real life Indian examples and explain step by step. Question: {prompt}""" 
                response = model.generate_content(full_prompt)
                st.write(response.text)
                
        st.session_state.messages.append({
            "role": "assistant",
            "content": response.text
        })
        
#Feature 2 - NCERT Helper
elif feature =="📚 NCERT Helper":
    st.header("📚 NCERT Helper")
    st.write("Get help with any NCERT topic from class 6 to 12!")
    
    col1, col2 = st.columns(2)
    subject = col2.selectbox(
        "Select Class:",
        ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"]
    )
    with col1:
        class_level = st.selectbox(
            "Select Subject:",
            ["Mathematics","Science","Physics",
             "Chemistry","Biology","History",
             "Geography","Economics","English"]
        )
        
    topic = st.text_input("Enter the topic or chapter name:")
    query_type = st.radio(
        "What do you need?",
        ["Explain the concept",
         "Give me examples",
         "Summarize the chapter",
         "Important points for exam"]
    )
    
    if st.button("Get Help"):
        with st.spinner("Fetching NCERT help..."):
            prompt = f"""You are an expert NCERT teacher for Indian students. {get_language_prompt(language)}
            {query_type} for {class_level} {subject} topic:{topic}
            Use simple language, real life Indian examples and explain step by step.
            Format your answer clearly with headings and points."""
            response = model.generate_content(prompt)
            st.success("Here's your NCERT help!")
            st.write(response.text)
    else:
        st.warning("Please enter a topic and select what help you need.")
        
#Feature 3 - Exam Preparation
elif feature =="📄 Exam Preparation":
    st.header("📄 Exam Preparation")
    st.write("Get personalized study plans, important questions and tips for your exams!")
    
    col1, col2, col3= st.columns(3)
    with col1:
        class_level = st.selectbox(
            "Class:",
            [f"Class {i}" for i in range(6,13)]
        )
    with col2:
        subject = st.selectbox(
            "Subject:",
            ["Mathematics","Science","Physics",
             "Chemistry","Biology","History",
             "Geography","Economics","English"]
        )
    with col3:
        question_type = st.selectbox(
            "Question Type:",
            ["Short Answer", "Long Answer", "Multiple Choice","Fill in the blanks"]
        )
    
    topic = st.text_input("Enter the topic or chapter name:")
    num_questions = st.slider("Number of questions:", 1, 20, 5)
    
    if st.button("Generate Questions"):
        if topic:
            with st.spinner("Generating exam questions..."):
                prompt = f"""You are an expert exam coach for Indian students. {get_language_prompt(language)}
                Generate {num_questions} {question_type} questions for {class_level} {subject} topic: {topic}.
                Provide clear answers and explanations for each question."""
                response = model.generate_content(prompt)
                st.success("Here are your exam questions!")
                st.write(response.text)
        else:
            st.warning("Please enter a topic to generate questions.")
            
#Feature 4 - Teacher Assistance
elif feature =="🧑‍🏫 Teacher Assistance":
    st.header("🧑‍🏫 Teacher Assistance")
    st.write("Get help with lesson planning, creating quizzes and more!")
    
    task = st.radio(
        "What do you need help with?",
        ["Create Lesson Plan",
         "Generate Worksheet",
         "Explain Difficult Concept Simply",
         "Create Assignment Questions"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        class_level = st.selectbox(
            "Class:",
            [f"Class {i}" for i in range(6,13)]
        )
    with col2:
        subject = st.selectbox(
            "Subject:",
            ["Mathematics","Science","Physics",
             "Chemistry","Biology","History",
             "Geography","Economics","English"]
        )
    
    topic = st.text_input("Enter the topic or chapter name:")
    
    if st.button("Generate"):
        if topic:
            with st.spinner("Generating teacher assistance..."):
                prompt = f"""You are an expert teacher assistant for Indian educators. {get_language_prompt(language)}
                Task: {task}
                Class: {class_level}
                Subject: {subject}
                Topic: {topic}
                Provide clear and practical resources that can be used directly to implement {task} in the classroom."""
                response = model.generate_content(prompt)
                st.success(f"{task}!")
                st.write(response.text)
        else:
            st.warning("Please enter a topic to get teacher assistance.")
            
#Feature 5 - Performance Tracker
elif feature =="📊 Performance Tracker":
    st.header("📊 Performance Tracker")
    st.write("Track your learning progress and get personalized feedback!")
    
    st.subheader("Enter your Marks:")
    col1,col2= st.columns(2)
    
    subjects = {}
    with col1:
        subjects["Mathematics"] = st.number_input("Mathematics", min_value=0, max_value=100, step=1)
        subjects["Science"] = st.number_input("Science", min_value=0, max_value=100, step=1)
        subjects["English"] = st.number_input("English", min_value=0, max_value=100, step=1)
    with col2:
        subjects["History"] = st.number_input("History", min_value=0, max_value=100, step=1)
        subjects["Geography"] = st.number_input("Geography", min_value=0, max_value=100, step=1)
        subjects["Economics"] = st.number_input("Economics", min_value=0, max_value=100, step=1)
        
    if st.button("Analyze My Performance"):
        with st.spinner("Analyzing performance..."):
            avg = sum(subjects.values())/len(subjects)
            
            #Show metrices
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Score", f"{avg:.2f}%")
            with col2:
                best = max(subjects, key=subjects.get)
                st.metric("Best Subject", best)
            with col3:
                worst = min(subjects, key=subjects.get)
                st.metric("Needs Improvement", worst)
                
            #Get AI Advice
            prompt = f"""A Rural Indian student has the following marks:{subjects}.
            The average score is {avg:.2f}%. The best subject is {best} and the subject that needs improvement is {worst}.
            {get_language_prompt(language)}
            Give speciic, encouraging and practical study advice.
            Focus on how to improve in {worst} while maintaining strengths in {best}. 
            Consider they may not have access to internet or extra resources."""
            response = model.generate_content(prompt)
            st.success("Personalized Study Advice:")
            st.write(response.text)