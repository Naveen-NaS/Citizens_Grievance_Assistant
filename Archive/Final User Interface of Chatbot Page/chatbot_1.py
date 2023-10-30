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
    responses = {}
    for question_data in intents['intents'][2]['options']:  # Use the 'complaint' intent (index 2)
        tag = question_data['tag']
        question = question_data['question']

        # If there are choices provided, present them to the user
        if 'choices' in question_data:
            choices = question_data['choices']
            print(f"{bot_name}: {question}")
            for i, choice in enumerate(choices, start=1):
                print(f"{i}. {choice}")
            user_choice = input("You (Enter the number corresponding to your choice): ")
            responses[tag] = choices[int(user_choice) - 1]  # Convert user input to the selected choice
        else:
            user_response = input(f"{bot_name} : {question}\nYou: ")
            responses[tag] = user_response

    print("Confirm Your Grievance: ")
    for tag, response in responses.items():
        print(f"{tag}: {response}")
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
                handle_complaint()  # Call the handle_complaint function for complaint handling
                break
            elif tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
                break
    else:
        print(f"{bot_name}: I do not understand...")
