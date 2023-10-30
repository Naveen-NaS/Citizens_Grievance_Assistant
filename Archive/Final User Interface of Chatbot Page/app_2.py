from flask import Flask, render_template, request, jsonify
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from pywebio.input import *
from pywebio.output import *
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from pywebio.session import *

app = Flask(__name__)

# Load your chatbot data and model here
# Make sure to adjust the file paths as needed
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

bot_name = "CG-Assistance"

# Create a dictionary to store user responses
user_responses = {}

# Flag to track whether the user has requested the exam
exam_requested = False

# Define the exam questions
exam_questions = [
    ("Q1. Which government type are you addressing ?", ["Central Government", "State Government"]),
    ("Q2. Which Ministry/Department is involved?", ["Home Affairs", "Housing And Urban Affairs", "Health & Family Welfare", "Central Board of Direct Taxes(Income Tax)", "Labour And Employment Related", "Posts", "Telecommunications", "Personnel and Training", "Financial Services(Banking Division)", "Financial Services(Insurance Division)"]),
    ("Q3. Where is the issue located?", ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman & Nicobar Islands", "Chandigarh", "Dadra & Nagar Haveli & Daman & Diu (merged)", "Lakshadweep", "Delhi (National Capital Territory of Delhi)", "Puducherry"]),
    ("Q4. Please describe the problem or grievance in detail: ", None)
]

def handle_complaint():
    global exam_requested
    exam_requested = True  # Set the flag to indicate that the user has requested the exam
    user_responses.clear()  # Clear previous user responses

    put_markdown("You have requested to register a complaint. Let's begin the exam to register your grievance.")

    # Start the exam by sending the first question as a chatbot message
    send_question(0)

def send_question(question_index):
    question, options = exam_questions[question_index]
    put_markdown(f"**{question}**")
    if options:
        user_responses['q' + str(question_index + 1)] = options  # Store options in user_responses for later use
        put_buttons(options, onclick=lambda opt, question_index=question_index: handle_exam_response(opt, question_index))

def handle_exam_response(selected_option, question_index):
    user_responses['q' + str(question_index + 1)] = selected_option
    if question_index < len(exam_questions) - 1:
        # Send the next question
        send_question(question_index + 1)
    else:
        # All questions answered, display a message or perform further processing
        display_exam_results()

def display_exam_results():
    # Process user_responses and display the results
    # You can use user_responses to access the user's answers to each question
    # For example, user_responses['q1'] will give the answer to the first question
    # You can implement your logic to display or process the results here
    # Once you have processed the results, you can send a final message to the user

    put_markdown("Thank you for completing the application. Your grievance is registered.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global exam_requested
    user_message = request.form['user_message']
    bot_response = "Welcome to Citizens Grievance Assistant! What can I help you with?"

    # Your chatbot logic here
    sentence = user_message
    sentence = tokenize(sentence)
    x = bag_of_words(sentence, all_words)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x).float()

    output = model(x)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == "complaint":
                handle_complaint()  # Call the handle_complaint function to initiate the exam
            elif tag == intent["tag"]:
                bot_response = random.choice(intent['responses'])
    else:
        bot_response = "I do not understand..."

    response = {
        'bot_message': bot_response
    }

    if exam_requested:
        exam_requested = False  # Reset the exam request flag
        response['exam_requested'] = True  # Add a flag to indicate that the exam is requested
        response['exam_message'] = "You have requested to register a complaint. Let's begin to register your grievance."

    return jsonify(response)

@app.route('/exam', methods=['GET', 'POST'])
def start_exam():
    global exam_requested
    if exam_requested:
        exam_requested = False  # Reset the exam request flag
        return webio_view(send_question, question_index=0)
    else:
        return "No Grievance requested."

if __name__ == '__main__':
    app.run(debug=True)
