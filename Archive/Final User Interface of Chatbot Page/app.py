from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize the conversation state
conversation_state = 0

# Define the conversation steps
conversation_steps = [
    "🌟 Hello! Welcome to Citizens’ Grievance Assistant! What can I help you with? 1. Check the status of an existing grievance. 2. Register a Grievance.",
    "You've chosen to register a grievance. Is your grievance related to the: <br>1. Central Government Department <br> 2. State Government Department",
    "Great! You've selected the Central Government Department. Now, please enter your state /union territory",
    "Please choose one of the following departments:\n 1. Education Department\n2. Environment and Forest Department\n3. Health and Family Welfare Department\n4. Home Department\n5. Public Works Department (PWD)\n6. Social Welfare Department\n7. Tourism Department\n8. Transport Department\n9. Urban Development Department\n10. Women and Child Development Department",
    "Please enter Grievance Description",
    "Alright, thank you for submitting your grievance, Mrs. Dev. 🙌. I understand the seriousness of the situation and will keep you updated about its progress. To access your grievance updates in the future, simply return to our platform and login through your credentials. Have a wonderful day ! 😊",
]
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_state
    user_message = request.form.get('user_message')

    if conversation_state >= len(conversation_steps):
        # Conversation is complete
        return jsonify({"bot_message": "Thank you for chatting. The conversation is complete."})

    bot_message = conversation_steps[conversation_state]
    conversation_state += 1

    return jsonify({"bot_message": bot_message})

if __name__ == '__main__':
    app.run(debug=True ,port = 5002)