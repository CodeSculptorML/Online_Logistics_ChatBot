from flask import Flask, render_template, request

app = Flask(__name__)

# Your chatbot logic goes here
import nltk
from nltk.chat.util import Chat, reflections

extended_price_negotiation_pairs = [
    ["hi|hello|hey", ["Hello I'm the Online Virtual Assistant.I'm here to help you with your questions regarding logistics services"]],
    ["How are you?", ["I am doing well,How are you?"]],
    ["I am fine.I have some doubts", ["Please ask me your questions about products and services."]],
    ["when will my package be delivered?", ["can you please send me your tracking ID ? so that i can check the estimated time of delivery."]],
    ["Sure,here is my tracking ID ABD34Y6J", ["Thanks for providing tracking ID.Let me check."]],
    [" okay", ["Your package with tracking number ABD34Y6J is currently in transit and expected to be delivered in 3-4 days."]],
    ["Can you help me schedule a pickup for a package?", ["Of course! Please provide the pickup address, package dimensions, weight, and preferred pickup date and time."]],
    ["The pickup address is 123 Main St, Anytown, USA. The package is 12\" x 8\" x 6\" and weighs 5 lbs. I'd like it to be picked up tomorrow between 10 AM and 12 PM.", ["Got it! Your pickup has been scheduled for tomorrow between 10 AM and 12 PM at 123 Main St, Anytown, USA."]],
    ["I need assistance with customs clearance for an international shipment.", ["Sure thing! Could you provide me with the details of the shipment, including the contents, declared value, and destination country?"]],
    ["It's a shipment of electronics with a declared value of $1000, and it's going to France.", ["Thank you. I'll provide you with the necessary customs documentation and requirements for shipping electronics to France."]],
    ["What are the shipping options for overnight delivery?", ["We offer several overnight shipping options, including express air, priority ground, and same-day delivery in select areas. Can you provide me with the origin and destination zip codes, as well as the package dimensions and weight?"]],
    ["The package is shipping from 987 Elm St, Cityville, to 456 Oak St, Townsville. It's 10\" x 6\" x 4\" and weighs 2 lbs.", ["Thank you. Based on the information provided, I recommend our express air option for guaranteed overnight delivery. Would you like to proceed with that?"]],
    ["I need to change the delivery address for my package.", ["Sure thing! Please provide me with the tracking number and the new delivery address."]],
    ["The tracking number is ABD34Y6J, and the new address is 789 Maple Ave, Villagetown.", ["Thanks for providing the information. I've updated the delivery address for tracking number ABD34Y6J to 789 Maple Ave, Villagetown."]],

    ["help", ["Sure, How can i help you ? "]],
    ["bye|goodbye", ["Goodbye! If you have any more questions, feel free to ask."]],
    ["Thank You|Thanks|thnx", ["I am Glad that i was able to help you,Have a nice day !!"]],
]

extended_price_negotiation_chatbot = Chat(extended_price_negotiation_pairs, reflections)

def chatbot_response(user_input):
    response = extended_price_negotiation_chatbot.respond(user_input)
    if response:
        return response
    else:
        return "I'm sorry, I didn't understand that. Could you please ask me something else?"

# Flask routes
@app.route("/")
def index():
    # Since there's no need for index.html, redirect to chat.html
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("user_input")
    
    # Your chatbot logic goes here
    bot_response = chatbot_response(user_input)
    return render_template("chat.html", user_input=user_input, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
