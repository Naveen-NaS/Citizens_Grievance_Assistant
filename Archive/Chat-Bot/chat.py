import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Load intents data
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

# Load model and data
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

# Initialize the model
model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

# Function to handle options for all intents
def handle_options(intent_data):
    responses = {}
    for question_data in intent_data['options']:
        tag = question_data['tag']
        question = question_data['question']

        # If there are choices provided, present them to the user
        if 'choices' in question_data:
            choices = question_data['choices']
            responses[tag] = choices
        else:
            user_response = input(f"{bot_name} : {question}\nYou: ")
            responses[tag] = user_response

    return responses

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
    X = torch.from_numpy(X).float()

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent_data in intents['intents']:
            if 'options' in intent_data:
                responses = handle_options(intent_data)  # Display and handle options for the current intent
                print("Options:")
                for tag, choices in responses.items():
                    print(f"{tag}: {', '.join(choices)}")
                ch = input("You: ")
                if ch.lower() == 'yes':
                    print('Request Successfully Submitted')
                else:
                    pass
                break  # Break the loop after handling options for one intent
            elif tag == intent_data["tag"]:
                print(f"{bot_name}: {random.choice(intent_data['responses'])}")
                break
    else:
        print(f"{bot_name}: I do not understand...")
