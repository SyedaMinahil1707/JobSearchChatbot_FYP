import streamlit as st
from serpapi.google_search_results import GoogleSearchResults 


st.set_page_config(
    page_title="Job Searching Chatbot",
    page_icon=":briefcase:",
    layout="wide",
)

st.title("Job Searching Chatbot")
st.sidebar.title("Job Searching Chatbot")

style = """
    <style>
        body {
            color: #333;
            background-color: #f4f4f4;
            font-family: 'Arial', sans-serif;
        }
        .chat-container {
            width: 80%;
            margin: auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background-color: #fff;
        }
        .user-message {
            background-color: #e6f7ff;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .assistant-message {
            background-color: #000000;
            color: white;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .chat-input {
            width: 80%;
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            outline: none;
        }
        .chat-btn {
            margin-top: 10px;
        }
        .expander-content {
            padding: 0 20px;
        }
        .custom-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        .feedback-container {
            margin-top: 20px;
        }
    </style>
"""

st.markdown(style, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "job_results" not in st.session_state:
    st.session_state.job_results = []

job_description = ""

for item in st.session_state.messages + st.session_state.job_results:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

job_questions = [
    "SALAM",
    "SALAMALAIKUM",
    "ASSALAMUALAIKUM",
    "ASSALAMOALAIKUM",
    "ASSALAM U ALAIKUM"
    "ASSALAM O ALAIKOM",
    "ASSALAMOALAIKUM",
    "HELLO",
    "EMPLOYMENT",
    "HOW ARE YOU",
    "I WANT JOB",
    "YES",
    "BY",
]

responses = {
    "SALAM": "WALAIKOM ASSALAM! How can I assist you with your job search?",
    "SALAMALAIKUM": "WALAIKOM ASSALAM! How can I assist you with your job search?",
    "ASSALAMUALAIKUM": "WALAIKOM ASSALAM! How can I assist you with your job search?",
    "ASSALAMOALAIKUM": "WALAIKOM ASSALAM! How can I assist you with your job search?",
    "ASSALAM U ALAIKUM": "WALAIKOM ASSALAM! How can I assist you with your job search?",
    "ASSALAM O ALAIKOM": "WALAIKOM ASSALAM! How can I assist you with your job search?",
    "ASSALAMOALAIKUM": "WALAIKOM ASSALAM! How can I assist you with your job search?",
    "HELLO": "Hello! How can I assist you with your job search?",
    "EMPLOYMENT": "Sure, tell me more about the type of employment you are looking for.",
    "HOW ARE YOU": "I'm just a chatbot, but thanks for asking! How can I help you today?",
    "I WANT JOB": "Enter your job description",
    "YES": "Great! What specific job are you interested in?",
    "BY": "Goodbye! If you have more questions, feel free to ask.",
}

def clear_chat_history():
    st.session_state.messages = []
    st.session_state.job_results = []
    with open("chathistory.txt", "w") as file:
        for item in st.session_state.messages + st.session_state.job_results:
            file.write(f"{item['role']}: {item['content']}\n")

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
st.sidebar.markdown("<div class='custom button'></div>", unsafe_allow_html=True)


st.sidebar.markdown("## Customer Feedback:")
feedback = st.sidebar.text_area("Provide feedback of chatbot:")
if st.sidebar.button("Submit Feedback"):
    with open("feedback.txt", "a") as feedback_file:
        feedback_file.write(f"{feedback}\n")
    st.sidebar.success("Feedback submitted successfully!")

def save_to_chat_history(role, content):
    st.session_state.messages.append({"role": role, "content": content})
    with open("chathistory.txt", "a") as file:
        file.write(f"{role}: {content}\n")

def serpapi_search(query):
    try:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            search_params = {
                "q": query + " jobs",
                "api_key": "aa9376e3b6107fb3e2ae0eb1284c28de5a904793a977ec7f37e17b7427e1d1bf"
            }

            search = GoogleSearchResults(search_params)  # Updated instantiation
            result = search.get_dict()
            return result.get("organic_results", [])

    except Exception as e:
        # Handle the exception and return an error message
        return f"Error: {str(e)}"


def display_serpapi_jobs(serpapi_results):
    for index, result in enumerate(serpapi_results, start=1):
        title = result.get('title', '')
        company = result.get('snippet', '')
        link = result.get('link', '')

        with st.expander(f"Job {index} - {title}"):
            st.write(f"Company: {company}")
            st.write(f"Link: {link}")

if prompt := st.chat_input("Enter your desired job (example: Software Engineer)"):
    save_to_chat_history("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    job_description = prompt.upper()

    # Check if the user's input contains any of the job-related questions
    contains_job_question = any(question in job_description for question in job_questions)

    # Initialize response with a default message
    response = "I'm sorry, I didn't understand that. How can I assist you with your job search? Enter your description."

    if contains_job_question:
        # User input contains a job-related question, process accordingly
        role_response = "assistant"

        # Check if the job_description is in the responses dictionary
        if job_description in responses:
            response = responses[job_description]
        elif "JOB" in job_description:
            # Extract the job title from the user's input
            job_title = job_description.replace("JOB", "").strip()
            # Trigger job search for the specified position
            search_query = f"{job_title} jobs"
            serpapi_results = serpapi_search(search_query)
            if isinstance(serpapi_results, list):
                # Display the job search results
                display_serpapi_jobs(serpapi_results)
                st.session_state.job_results.append({"role": "assistant", "content": serpapi_results})
                save_to_chat_history("assistant", "Job search results displayed.")
                response = ""  # Set response to empty as the job search results are displayed
            else:
                # Display the error message
                response = serpapi_results

        # Save the response to chat history
        save_to_chat_history(role_response, response)

        # Display the response
        with st.chat_message(role_response):
            st.markdown(response)
    else:
        # User input does not contain a job-related question, trigger job search
        search_query = f"{job_description} jobs"
        serpapi_results = serpapi_search(search_query)

        if isinstance(serpapi_results, list):
            st.write("")
            display_serpapi_jobs(serpapi_results)
            st.session_state.job_results.append({"role": "assistant", "content": serpapi_results})
            save_to_chat_history("assistant", "Job search results displayed.")
        else:
            # Display the error message
            with st.chat_message("assistant"):
                st.markdown(serpapi_results)
