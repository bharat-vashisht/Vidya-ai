# Vidya AI — Technical Documentation

## Architecture Overview
Vidya AI is built using a three layer architecture:
- **Frontend:** Streamlit — Python based web framework
- **AI Layer:** Google Gemma 4 (gemma-4-26b-a4b-it) via Google AI Studio
- **Backend:** Python with google-genai library

## How Gemma 4 is Used
Vidya AI uses Gemma 4 as its core AI engine for:
1. Natural language understanding of student questions
2. Generating NCERT aligned explanations
3. Creating exam questions and quizzes
4. Providing personalized study advice
5. Supporting 10 Indian languages

## Features Deep Dive

### 1. Ask Vidya
- Uses Gemma 4 to answer any study question
- Prompt engineered to give simple, India relevant answers
- Supports 10 Indian languages
- Maintains conversation history using Streamlit session state

### 2. NCERT Helper
- Covers Class 6-12 all major subjects
- Four query types: explain, examples, summarize, exam points
- Aligned with Indian NCERT curriculum

### 3. Exam Preparation
- Generates MCQ, Short Answer, Long Answer questions
- Customizable number of questions (1-10)
- Provides answers and explanations

### 4. Teacher Assistant
- Creates lesson plans for any topic
- Generates worksheets and assignments
- Designed for low resource classrooms

### 5. Performance Tracker
- Analyzes student marks across subjects
- Identifies strongest and weakest subjects
- Provides personalized AI study advice

### 6. Quiz Mode
- Interactive quiz with real time scoring
- Progress bar and score tracking
- Balloon celebration on completion
- AI powered feedback after quiz

## Language Support
Vidya AI supports 10 Indian languages:
English, Hindi, Tamil, Telugu, Bengali,
Marathi, Gujarati, Kannada, Odia, Punjabi

## Reliability
- Primary model: gemma-4-26b-a4b-it
- Backup model: gemma-3-12b-it
- Automatic fallback if primary model unavailable

## Impact
- Target users: 600 million+ rural Indians
- Age group: 11-18 years (Class 6-12)
- Also helps teachers in low resource schools
- Works in native Indian languages

## Future Plans
- Voice input and output support
- Offline mode using smaller Gemma models
- Mobile app version
- Integration with government school curriculum
- Parent progress tracking dashboard

## Tech Stack
| Technology | Purpose |
|---|---|
| Python 3.14 | Core programming language |
| Streamlit | Web interface |
| Google Gemma 4 | AI engine |
| google-genai | API library |
| python-dotenv | Environment management |

## Challenges Faced
1. Model availability — solved with primary/backup system
2. Language support — solved with prompt engineering
3. Quiz parsing — solved with structured prompt format
4. Streamlit Cloud deployment — solved with correct requirements

## About the Developer
Bharat Vashisht
2nd Year Computer Science Student
GitHub: github.com/bharat-vashisht
Kaggle: kaggle.com/bharatvashisht