from flask import Flask, render_template, request,redirect,url_for,session
import difflib
import random

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# Initial chatbot responses
extended_logistics = [
    ["delivery date", ["Please let me know you tracking ID."]],
    ["Tracking Id - ABD34Y6J", ["Fetching your Transit information....."]],
    ["Change Delivery location", ["Sure provide me with your Tracking Id.I will Check"]],
    ["Assistance with my Tracking package", ["Hi there! I'd be happy to help you with that. Could you please provide me with the tracking number or order ID?"]],
    ["Can you provide the current location of the package?", ["Absolutely! Let me retrieve the latest location for you. Your package is currently at our distribution center in Gujarat,India. It will be sorted and dispatched for delivery later today. Is there anything else you'd like to know?"]],
    ["That's helpful, thank you. Can you also confirm the delivery address?", ["Of course! Let me double-check that for you. Your package is scheduled for delivery to 123 ABC street,Gandhipuram,Coimbatore,Tamil Nadu,India. Is there anything else I can assist you with?"]],
    ["No, that's all for now. Thank you for your help!", ["You're welcome! If you have any more questions or need further assistance, feel free to reach out. Have a great day!"]],
    ["Product Details", ["Let me Fetch that for you......Your product is self drilling screws from Shanghai Airport loaded in three containers currently in transit"]],
    ["You Are wrong", ["I am sorry for the response,Please enter something else"]],
    ["when will my package be delivered?", ["Can you please send me your tracking ID? I'll check the estimated time of delivery."]],
    ["Sure, here is my tracking ID ABD34Y6J", ["Thanks for providing the tracking ID. Let me check."]],
    ["okay", ["Your package with tracking number ABD34Y6J is currently in transit and expected to be delivered in 3-4 days."]],
    ["change address", ["Okay you can change your address.Kindly enter the new address"]],
    ["Can you help me schedule a pickup for a package?", ["Of course! Please provide the pickup address, package dimensions, weight, and preferred pickup date and time."]],
    ["The pickup address is 123 ABC street,Gandhipuram,Coimbatore,Tamil Nadu,India. The package is 12\" x 8\" x 6\" and weighs 5 lbs. I'd like it to be picked up tomorrow between 10 AM and 12 PM.", ["Got it! Your pickup has been scheduled for tomorrow between 10 AM and 12 PM at 123 Main St, Anytown, USA."]],
    ["I need assistance with customs clearance for an international shipment.", ["Sure thing! Could you provide me with the details of the shipment, including the contents, declared value, and destination country?"]],
    ["It's a shipment of electronics with a declared value of $1000, and it's going to France.", ["Thank you. I'll provide you with the necessary customs documentation and requirements for shipping electronics to France."]],
    ["What are the shipping options for overnight delivery ", ["We offer several overnight shipping options, including express air, priority ground, and same-day delivery in select areas. Can you provide me with the origin and destination zip codes, as well as the package dimensions and weight?"]],
    ["The package is shipping from Gujarat,India. It's 10\" x 6\" x 4\" and weighs 2 lbs.", ["Thank you. Based on the information provided, I recommend our express air option for guaranteed overnight delivery. Would you like to proceed with that?"]],
    ["I need to change the delivery address for my package.", ["Sure thing! Please provide me with the tracking number and the new delivery address."]],
    ["The tracking number is ABD34Y6J, and the new address is 456, XYZ Road,RS Puram,Coimbatore,Tamil Nadu,India", ["Thanks for providing the information. I've updated the delivery address for tracking number ABD34Y6J to 456, XYZ Road,RS Puram,Coimbatore,Tamil Nadu,India"]],

    ["help", ["Sure, how can I help you?"]],
    ["bye|goodbye", ["Goodbye! If you have any more questions, feel free to ask."]],
    ["Thank You|Thanks|thnx", ["I am glad that I was able to help you. Have a nice day!"]],
    ["hi|hello|hey", ["Hello I'm the Online Virtual Assistant. I'm here to help you with your questions regarding logistics services.Please Enter Your Tracking ID so that i can assist better"]],
    ["How are you?", ["I am doing well, how about you?Please Enter Your Tracking ID so that i can assist better"]],

    ["ABD34Y6J", ["Fetching your Transit information....."]],
    ["ABD56FGQ", ["Fetching your Transit information....."]],
    ["JY673545", ["Fetching your Transit information....."]],
    ["I am fine. I have some doubts", ["I would be very happy to help you.How Can I assist you :<br>1.Delivery Date <br>2.Change Delivery Location <br> 3.Current Delivery Address <br> 4.Product Details <br> 5.Other"]],
    ["some doubts", ["I would be very happy to help you.How Can I assist you :<br>1.Delivery Date <br>2.Change Delivery Location <br> 3.Current Delivery Address  <br> 4.Other"]],
    ["Assistance", ["I would be very happy to help you.How Can I assist you :<br>1.Delivery Date <br>2.Change Delivery Location <br> 3.Current Delivery Address <br> 4.Other"]],
    ["Assist me", ["I would be very happy to help you.How Can I assist you :<br>1.Delivery Date <br>2.Change Delivery Location <br> 3.Current Delivery Address <br> 4.Other"]],
    ["1.", ["Your package with tracking number ABD34Y6J is currently in transit and expected to be delivered in 3-4 days."]],
    ["2.", ["Sure thing! Please provide me with the new delivery address."]],
    ["the new address is 456, XYZ Road,RS Puram,Coimbatore,Tamil Nadu,India", ["Thanks for providing the information. I've updated the delivery address for tracking number ABD34Y6J to456, XYZ Road,RS Puram,Coimbatore,Tamil Nadu,India "]],
    ["3.", ["Of course! Let me double-check that for you. Your package is scheduled for delivery to 123 ABC street,Gandhipuram,Coimbatore,Tamil Nadu,India. Is there anything else I can assist you with?"]],
    ["4.", ["Please Enter your Query."]],
    
]

delivery_addresses = [
    "123 ABC street, Gandhipuram, Coimbatore, Tamil Nadu, India",
    "456 XYZ Road, RS Puram, Coimbatore, Tamil Nadu, India",
    "789 PQR Avenue, Peelamedu, Coimbatore, Tamil Nadu, India",
    "321 LMN Lane, Saibaba Colony, Coimbatore, Tamil Nadu, India",
    "987 EFG Street, Ramanathapuram, Coimbatore, Tamil Nadu, India"
]
# Login route

# Flask routes
@app.route("/")
def index():
   # Since there's no need for index.html, redirect to chat.html
    return render_template("login.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("user_input")
    #user_input = "Hi"
    if user_input is None:
        user_input = "Hi"
    else:
        user_input = request.form.get("user_input")
    # Get response
    bot_response = get_response(user_input)
    
    # Update response pairs if bot doesn't know the answer
    if bot_response == "I'm sorry, I didn't understand that. Could you please ask me something else?":
        update_response_pairs(user_input)
        bot_response = "I have updated my knowledge. Please ask me again."
    
    return render_template("chat.html", user_input=user_input, bot_response=bot_response)

# Function to get the closest match response
def get_response(user_input):
    user_input_lower = user_input.lower()
    response = None

    for tracking_id in ["ABD34Y6J", "ABD56FGQ", "JY673545"]:
        if tracking_id.lower() in user_input_lower:
            session["tracking_id"] = tracking_id
            response = f"Hey, your package with tracking ID {tracking_id} is currently in transit."
            return response
    
    for pattern, replies in extended_logistics:
        if any(word in user_input_lower for word in pattern.split('|')):
            response = replies[0]
            break

    if not response:
        closest_match = difflib.get_close_matches(user_input_lower, [pattern.split('|')[0] for pattern, _ in extended_logistics], n=1)
        if closest_match:
            response = [replies for pattern, replies in extended_logistics if pattern.split('|')[0] == closest_match[0]][0][0]
        else:
            response = "Please ask me questions only about Delivery status and shipping services"

    #if "change delivery location" in user_input_lower or "2" in user_input_lower:
     #   response = "Sure, please provide me with your tracking ID."
      #  session["change_delivery_location"] = True
    
    # Handle updating delivery address
    #elif session.get("change_delivery_location"):
     #   response = f"Okay, I have updated your delivery address to {user_input}."
      #  session.pop("change_delivery_location", None)
            
    # Handle adding new delivery location
    if "change delivery location" in user_input_lower or "2." in user_input_lower:
        # Check if tracking ID is already stored in session
        if "tracking_id" in session:
            response = "Okay, please provide me with the new delivery address."
        else:
            response = "Sure, please provide me with your tracking ID."
    
    # Handle updating delivery address
    elif "tracking_id" in session:
        new_delivery_address = user_input
        tracking_id = session["tracking_id"]
        response = f"Okay, I have updated your delivery address for tracking ID {tracking_id} to {new_delivery_address}."
        session.pop("tracking_id")


    if "current delivery address" in user_input_lower or "3" in user_input_lower:
        current_delivery_address = random.choice(delivery_addresses)
        response = f"Your current delivery address is {current_delivery_address}."

    if "1" in user_input_lower or "delivery date" in user_input_lower:
        random_days = random.choice(["1-2", "3-4", "5-7"])
        response = f"Your package with tracking number {tracking_id} is currently in transit and expected to be delivered in {random_days} days."

    
            
    return response

# Function to update response pairs
def update_response_pairs(user_input):
    # Add user input as a new pattern with an empty response
    extended_logistics.append([user_input, [""]])

if __name__ == "__main__":
    app.run(debug=True)
