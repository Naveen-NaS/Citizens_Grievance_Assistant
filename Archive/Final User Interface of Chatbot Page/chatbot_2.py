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


# setup is above this line

# function start

def complaint():
    responses = {}

    menu_questions = [
        {"tag": "government_type", "question": "Which government type are you addressing (Central/State)?"},
        {"tag": "department", "question": "Which department/ministry is involved?"},
        {"tag": "location", "question": "Where is the issue located?"},
        {"tag": "problem_description", "question": "Please describe the problem or grievance in detail:"}
    ]

    for menu_item in menu_questions:
        tag = menu_item['tag']
        question = menu_item['question']
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


# function end

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
                complaint()
                break
            elif tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
                break
    else:
        print(f"{bot_name}: I do not understand...")