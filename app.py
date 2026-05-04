import streamlit as st
from dotenv import load_dotenv
from google import genai
import os
import time 

#Load API key
load_dotenv()

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error("❌ API KEY NOT FOUND")
    st.stop()

client = genai.Client(api_key=api_key)

#Page configuration
st.set_page_config(page_title="Vidya AI", page_icon="🎓", layout="wide")

# Custom CSS for better look
st.markdown("""
    <style>
         .stButton>button {
            background-color: #4a90e2;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #357abd;
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
language = st.sidebar.selectbox("Select Language", ["English", "Hindi","Telugu","Bengali","Marathi","Gujarati","Tamil","Kannada","Odia","Punjabi"]) 

#Feature selection
feature = st.sidebar.radio(
       "Select Feature", 
        ["💭 Ask VIDYA", 
         "📚 NCERT Helper", 
         "📄 Exam Preparation", 
         "🧑‍🏫 Teacher Assistance",
         "📊 Performance Tracker",
         "🎯 Quiz Mode"]) 

st.sidebar.markdown("---")
st.sidebar.markdown("Built for Gemma 4 Good Hackathon 2026")
st.sidebar.markdown("By **Bharat Sharma**")

if st.sidebar.button("TEST AI"):
    try:
        test = client.models.generate_content(
            model="models/gemma-4-26b-a4b-it",
            contents="Say hello"
        )
        st.success("AI WORKING ✅")
    except Exception as e:
        st.error(f"AI ERROR ❌: {e}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Helper function for language
def get_language_prompt(language):
        language_prompts = {
            "Hindi": "Answer in simple Hindi language that a rural Indian student can understand.",
            "Tamil": "Answer in simple Tamil language that a rural Indian student can understand.",
            "Telugu": "Answer in simple Telugu language that a rural Indian student can understand.",
            "Bengali": "Answer in simple Bengali language that a rural Indian student can understand.",
            "Marathi": "Answer in simple Marathi language that a rural Indian student can understand.",
            "Gujarati": "Answer in simple Gujarati language that a rural Indian student can understand.",
            "Kannada": "Answer in simple Kannada language that a rural Indian student can understand.",
            "Odia": "Answer in simple Odia language that a rural Indian student can understand.",
            "Punjabi": "Answer in simple Punjabi language that a rural Indian student can understand."
        }
        return language_prompts.get(language, "Answer in simple English that a rural Indian student can understand.")

def get_ai_response(prompt):
    try:
        response = client.models.generate_content(
            model="models/gemma-4-26b-a4b-it",
            contents=prompt
        )
        return response.text
    except Exception as e:
        try :
            response = client.models.generate_content(
                model="models/gemma-3-12b-it",
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error gettin response: {e}"
        
language_greetings = {
    "Hindi": "नमस्ते! मैं विद्या हूँ, मैं आपकी कैसे मदद कर सकती हूँ?",
    "Tamil": "வணக்கம்! நான் வித்யா, உங்கள் AI டியூட்டர். நான் உங்களுக்கு எப்படி உதவலாம்?",
    "Telugu": "నమస్తే! నేను విద్యా, మీ AI ట్యూటర్. నేను మీకు ఎలా సహాయం చేయగలను?",
    "Bengali": "নমস্কার! আমি বিদ্যা, আপনার AI টিউটর. আমি কিভাবে সাহায্য করতে পারি?",
    "Marathi": "नमस्कार! मी विद्या, तुमची AI ट्यूटर. मी तुम्हाला कशी मदत करू शकते?",
    "Gujarati": "નમસ્તે! હું વિદ્ય, તમારી AI ટ્યુટર. હું તમને કેવી રીતે મદદ કરી શકું?",
    "Kannada": "ನಮಸ್ಕಾರ! ನಾನು ವಿದ್ಯಾ, ನಿಮ್ಮ AI ಟ್ಯೂಟರ್. ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?",
    "Odia": "ନମସ୍କାର! ମୁଁ ଭିଦ୍ୟା, ଆପଣଙ୍କର AI ଟ୍ୟୁଟର. ମୁଁ ଆପଣଙ୍କୁ କିପରି ସହାୟତା କରିପାରିବି?",
    "Punjabi": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਵਿਦਿਆ, ਤੁਹਾਡੀ AI ਟਿਊਟਰ. ਮੈਂ ਤੁਹਾਨੂੰ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦੀ ਹਾਂ?"
}

placeholders = {
     "Hindi": "अपना सवाल यहाँ लिखें...",
    "Tamil": "உங்கள் கேள்வியை இங்கே எழுதுங்கள்...",
    "Telugu": "మీ ప్రశ్నను ఇక్కడ రాయండి...",
    "Bengali": "আপনার প্রশ্ন এখানে লিখুন...",
    "Marathi": "तुमचा प्रश्न येथे लिहा...",
    "Gujarati": "તમારો પ્રશ્ન અહીં લખો...",
    "Kannada": "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ...",
    "Odia": "ଆପଣଙ୍କ ପ୍ରଶ୍ନ ଏଠାରେ ଲିଖନ୍ତୁ...",
    "Punjabi": "ਆਪਣਾ ਸਵਾਲ ਇੱਥੇ ਲਿਖੋ...",
}

# Feature 1 - Ask VIDYA
if feature == "💭 Ask VIDYA":
    st.header("💭 Ask VIDYA Anything")
    st.write(language_greetings.get(language, "Your personal AI teacher - available 24/7 to help you with your studies!"))

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input(placeholder="Type your message here...")

    if prompt:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    full_prompt = f"You are VIDYA... {prompt}"

                    response = client.models.generate_content(
                        model="models/gemma-4-26b-a4b-it",
                        contents=full_prompt
                    )
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

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
        if topic:
            with st.spinner("Fetching NCERT help..."):
                prompt = f"""You are an expert NCERT teacher for Indian students. {get_language_prompt(language)}
                {query_type} for {class_level} {subject} topic:{topic}
                Use simple language, real life Indian examples and explain step by step.
                Format your answer clearly with headings and points."""
                try:
                    response = client.models.generate_content(
                        model="models/gemma-4-26b-a4b-it",
                        contents=prompt
                    )
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

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
                try:
                    response = client.models.generate_content(
                        model="models/gemma-4-26b-a4b-it",
                        contents=prompt
                    )
                    st.success("Here are your exam questions!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")
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
                try:
                    response = client.models.generate_content(
                        model="models/gemma-4-26b-a4b-it",
                        contents=prompt
                    )
                    st.success(f"{task}!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")
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
            try:
                response = client.models.generate_content(
                    model="models/gemma-4-26b-a4b-it",
                    contents=prompt
                )
            except Exception as e:
                st.error(f"AI Error: {e}")
            st.success("Personalized Study Advice:")
            st.write(response.text)
            
#Feature 6 - Quiz Mode
elif feature =="🎯 Quiz Mode":
    st.header("🎯 Quiz Mode")
    st.write("Test your knowledge with personalized quizzes!")
    
    #Initialize quiz state
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = []
        
    if not st.session_state.quiz_started:
        #Quiz setup
        col1, col2 = st.columns(2)
        with col1:
            class_level = st.selectbox(
                "Select Class:",
                [f"Class {i}" for i in range(6,13)]
            )
        with col2:
            quiz_subject = st.selectbox(
                "Select Subject:",
                ["Mathematics","Science","Physics",
                 "Chemistry","Biology","History",
                 "Geography","Economics","English"]
            )
            
        quiz_topic = st.text_input("Enter the quiz topic:")
        num_questions = st.slider("Number of questions:", 3, 20, 5)
        
        if st.button("Start Quiz"):
            if quiz_topic:
                with st.spinner("Generating quiz questions..."):
                    prompt = f"""Generate exactly {num_questions} MCQ 
                    questions for {class_level} {quiz_subject} 
                    on topic: {quiz_topic}
                    {get_language_prompt(language)}
                    
                    Format EXACTLY like this for each question:
                    Q: [question]
                    A) [option]
                    B) [option]
                    C) [option]
                    D) [option]
                    Answer: [correct letter]
                    
                    Number each question and separate with ---"""
                    
                    try:
                        response = client.models.generate_content(
                            model="models/gemma-4-26b-a4b-it",
                            contents=prompt
                        )
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"AI Error: {e}")
                    
                    # Parse Questions
                    questions = []
                    raw_questions = response.text.split("---")
                    for q in raw_questions:
                        if "Q:" in q and "Answer:" in q:
                            questions.append(q.strip())
                        
                    st.session_state.quiz_questions = questions
                    st.session_state.quiz_started = True
                    st.session_state.current_question = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_answers = []
            else:
                st.warning("Please enter a quiz topic to start.")
                
    else:
        #Quiz in progress
        total = len(st.session_state.quiz_questions)
        current = st.session_state.current_question
        
        if current < total:
            #Show progress
            st.progress((current)/total)
            st.write(f"Question {current+1} of {total}")
            st.metric("Current Score", f"{st.session_state.quiz_score} / {current}")
            
            #show question
            question = st.session_state.quiz_questions[current]
            st.markdown(f"**{question.split('Answer:')[0].strip()}**")
            
            #Get Answer
            answer = st.radio("Select your answer:", ["A", "B", "C", "D"],
                              key=f"answer_{current}")
            
            if st.button("Submit Answer", key=f"submit_{current}"):
                #Check answer
                correct = question.split("Answer:")[-1].strip()[0]
                if answer == correct:
                    st.success("Correct! 🎉")
                    st.session_state.quiz_score += 1
                else:
                    st.error(f"Wrong! The correct answer was {correct}.")
                    
                st.session_state.current_question += 1
                st.session_state.quiz_answers.append(
                    {"question": question, 
                     "your_answer": answer,
                     "correct_answer": correct,
                     "correct": answer == correct}
                )
                import time
                time.sleep(1)
                st.rerun()
            
        else:
            #Quiz completed
            score = st.session_state.quiz_score
            total = len(st.session_state.quiz_questions)
            percentage = (score/total)*100
            
            st.balloons()
            st.header("Quiz Completed!🎉")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Final Score", f"{score} / {total}")
            with col2:
                st.metric("Percentage", f"{percentage:.2f}%")
            with col3:
                if percentage >= 80:
                    st.metric("Performance", "Excellent! Keep it up! 🌟")
                elif percentage >= 50:
                    st.metric("Performance", "Good effort! A little more practice will help! 👍")
                else:
                    st.metric("Performance", "Don't worry! Review the material and try again! 💪")
                    
            #Show answer review
            st.subheader("Answer Review:")
            for ans in st.session_state.quiz_answers:
                if ans["correct"]:
                    st.markdown(f"✅ **{ans['question'].split('Answer:')[0].strip()}** - Your answer: {ans['your_answer']} (Correct)")
                else:
                    st.markdown(f"❌ **{ans['question'].split('Answer:')[0].strip()}** - Your answer: {ans['your_answer']} (Correct answer: {ans['correct_answer']})")
                    
            #Get AI feedback
            with st.spinner("Getting personalized feedback..."):
                prompt = f"""A student scored {score}/{total} 
                ({percentage:.1f}%) on a quiz.
                {get_language_prompt(language)}
                Give encouraging and specific advice to improve.
                Keep it short and motivating!"""
                try:
                    response = client.models.generate_content(
                        model="models/gemma-4-26b-a4b-it",
                        contents=prompt
                    )
                    st.info(response.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

            if st.button("Start New Quiz"):
                st.session_state.quiz_started = False
                st.session_state.quiz_questions = []
                st.session_state.quiz_score = 0
                st.session_state.current_question = 0
                st.session_state.quiz_answers = []
                st.rerun()