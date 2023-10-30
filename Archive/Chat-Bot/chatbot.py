import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# Function to handle the complaint process
def handle_complaint():
    responses = {}  # Dictionary to store user responses

    # Get the "complaint" intent from intents.json
    complaint_intent = [intent for intent in intents['intents'] if intent['tag'] == 'complaint'][0]

    counter = 0  # Initialize a counter
    for question_tag, question_data in complaint_intent['questions'].items():
        if counter >= 2:
            break
        question = question_data
        options = complaint_intent.get('options', {}).get(question_tag, None)

        # Present question and options to the user
        print(f"{bot_name}: {question}")
        if options:
            for i, option in enumerate(options, start=1):
                print(f"{i}. {option}")

            user_choice = input("You (Enter the number corresponding to your choice): ")
            selected_option = options[int(user_choice) - 1]
            responses[question_tag] = selected_option
        else:
            user_input = input(f"{bot_name} : {question}\nYou: ")
            responses[question_tag] = user_input

        # Check if there are follow-up responses for this question
        if question_tag in complaint_intent['follow_up_responses']:
            follow_up_response = complaint_intent['follow_up_responses'][question_tag]
            print(f"{bot_name}: {random.choice(follow_up_response)}")

    print("Confirm Your Grievance: ")
    for question_tag, response in responses.items():
        print(f"{question_tag}: {response}")
    ch = input("You: ")
    if ch.lower() == 'yes':
        print('Request Successfully Submitted')
    else:
        pass


# Chatbot working
bot_name = "CG-Assistance"
print("Welcome to Citizens Grievance Assistant! What can I help you with? (type 'quit' to exit)")

while True:
    sentence = input("You: ")
    if sentence.lower() == "quit":
        break

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == "complaint":
                print(f"{bot_name}: {random.choice(intent['responses'])}")
                handle_complaint()  # Call the handle_complaint function for complaint handling
                break
            elif tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
                break
    else:
        print(f"{bot_name}: I do not understand...")

