from flask import Flask
from flask import render_template, jsonify, request
import requests
from response import *
import random
from fuzzywuzzy import process

credit_card_thresh = 300


class Links:
    checkout_message = "You can checkout further information in the following link: "
    personal_loan_link = "personal loan"
    error_msg = "Sorry, we couldn't find any response!!"


def get_info_from_db_dict(parameter, db_info):
    choices = list(db_info)
    db_col = process.extractOne(parameter, choices)[0]
    return db_info[db_col]


def get_general_info_from_db(parameter):
    # connect to db and retrieve db dict.
    db_info = {'contact': "Bhushan: 8898546254"}
    return get_info_from_db_dict(parameter, db_info)


def get_user_specific_info(parameter):
    # connect to db and retrieve db dict.
    db_info = {'credit score': "350", 'balance': 20000, 'base limit': 1000, 'uname': 'RishabhBhatnagar'}
    return get_info_from_db_dict(parameter, db_info)


class IntentMapping:
    @staticmethod
    def card_charge(length, entity, value):
        value = value
        if length > 0 and entity == "card_type":
            if value == "debit card":
                response_text = "For debit card first year is free and from second year onward we charge 300tk per year"
            elif value == "credit card":
                response_text = "For credit cards we charge 500% per year"
            else:
                response_text = "I am not sure about that, sorry!"
        else:
            response_text = "For credit cards we charge 500% per year. And for debit cards first year is free and from second year we charge 300tk per year"
        return response_text

    @staticmethod
    def get_cheque_book():
        global chequeBookAddress
        chequeBookAddress = 1

    @staticmethod
    def loan(type, limit):
        return "We provide home loan of maximum 1.2 crore tk"

    @staticmethod
    def loan_details():
        return "We provide 3 different kinds of loans currently.\n1.Personal loan(Marriage, traveling, education etc)\n2.Car loan\n3.Home loan"

    @staticmethod
    def show_balance():
        return "Your current account balance is {}".format(get_user_specific_info('balance'))

    @staticmethod
    def summary():
        bal = get_user_specific_info('balance')
        base_limit = get_user_specific_info('base limit')
        return "Account type: Checking Account\nCurrent balance: {}.\nAvailable to withdraw: {}.".format(bal,
                                                                                                         bal - base_limit)

    @staticmethod
    def lost_card():
        information = get_general_info_from_db(parameter="emergency contact")
        for mandatory_string in ("lost", 'missed'):
            if mandatory_string in request.form["text"]:
                response_text = 'Try contacting:\n' + information
                break
        return response_text

    @staticmethod
    def loan_personal():
        credit_score = int(get_user_specific_info('credit score'))
        if credit_score < credit_card_thresh:
            response_text = "You are not eligible for loan.\n your credit score should be greater than {}".format(
                credit_card_thresh)
        else:
            response_text = 'You are eligible for the loan.\n' + Links.checkout_message + "\n" + Links.personal_loan_link
        return response_text

    @staticmethod
    def loan_min(length, value, entity):
        if length > 0 and entity == "loan":
            value = value
            if value == "medical" or value == "personal" or value == "marriage" or value == "traveling":
                response_text = "We provide minimum personal loan of 50,000 tk lacs tk"
            elif value == "car":
                response_text = "We provide car loan of minimum of 5 lacs tk"
            elif value == "home":
                response_text = "We provide home loan of minimum 20 lacs tk"
            elif value == "education":
                response_text = "We provide home loan of minimum 10k."
        return response_text

    @staticmethod
    def greet():
        try:
            uname = get_user_specific_info('user name')
            if uname is not None:
                return "Hello, {}. How may i help you??".format(uname)
            else:
                return "Hello user, How may i help you??"
        except:
            return "Hello user, How may i help you??"

    @staticmethod
    def loan_max(length, entity, value):
        response_text = None
        if length > 0 and entity == "loan":
            value = value
            if value == "medical" or value == "personal" or value == "marriage" or value == "traveling":
                response_text = "We provide personal loan of maximum 2 lacs tk"
            elif value == "car":
                response_text = "We provide car loan of maximum of 20 lacs tk"
            elif value == "home":
                response_text = "We provide home loan of maximum 1.2 crore tk"
            elif value == "education":
                response_text = 'we provide eduction loan upto 10 lacs.'
        return response_text


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')


get_random_response = lambda intent: random.choice(response[intent])
isClosingCard = False
chequeBookAddress = 0


@app.route('/chat', methods=["POST"])
def chat():
    global isClosingCard
    """
    chat end point that performs NLU using rasa.ai
    and constructs response from response.py
    """
    try:
        response = requests.get("http://localhost:5000/parse", params={"q": request.form["text"]})
        # response = requests.get("http://localhost:5000/parse?q="+request.form["text"])
        response = response.json()
        intent = response["intent"]
        intent = intent["name"]
        entities = response["entities"]
        length = len(entities)
        if length > 0:
            entity = entities[0]["entity"]
            value = entities[0]["value"]
        else:
            entity, value = None, None
        if intent == "event-request":
            response_text = get_event(entities["day"], entities["time"], entities["place"])
        # elif isClosingCard == True:
        #    if response["text"] == "1234":
        #        response_text = "We are closing this card. Thanks for your patience."
        #        isClosingCard = False

        #    elif response["text"] == "ok":
        #        response_text = "How else I can help you? :)"
        #        isClosingCard = False

        #    else:
        #        response_text = "This card doesn't exist. Please check the number again. If you want to talk about anything else rather than this #then type ok"
        # elif intent == "lost_card":
        # response_text = "Please give us your credit card number"
        # isClosingCard = True
        elif intent == "greet":
            response_text = IntentMapping.greet()
        elif intent == "card_charge":
            response_text = IntentMapping.card_charge(length, entity, value)
        elif intent == "get_cheque_book":
            response_text = IntentMapping.get_cheque_book()
        elif intent == "loan_car":
            response_text = IntentMapping.loan_personal()
        elif intent == "loan_home":
            response_text = "We provide home loan of minimum 20 lacs tk and maximum 1.2 crore tk"
        elif intent == "loan_max":
            response_text = IntentMapping.loan_max(length, entity, value)
        elif intent == "loan_min":
            response_text = IntentMapping.loan_min(length, value, entity)
        elif intent == "loan_details":
            response_text = IntentMapping.loan_details()
        elif intent == "show_balance":
            response_text = IntentMapping.show_balance()
        elif intent == "summary":
            response_text = IntentMapping.summary()
        elif intent == 'lost_card':
            response_text = IntentMapping.lost_card()
        elif intent == "loan_personal":
            response_text = IntentMapping.loan_personal()
        else:
            response_text = ''
        global chequeBookAddress
        print(chequeBookAddress, "chequeBookAddress")
        if chequeBookAddress == 1:
            # waiting for user to enter address for the first time.
            _response = jsonify({"status": "success", "response": "Enter your address: "})
            chequeBookAddress = chequeBookAddress + (1 << 1)
            return _response
        elif chequeBookAddress == 3:
            # chatbot already prompted for an address.
            # todo: validate address.
            if len(request.form['text']) > 5:
                chequeBookAddress = 0
                return jsonify({"status": "success",
                                "response": "Cheque book will be delivered to your address: \n{}."
                                            "\nNomial fees will be deducted from your bank account.".format(
                                    request.form['text'])})
            else:
                return jsonify({"status": "success", "response": "Please enter a valid address."})
        else:
            return jsonify({"status": "success", "response": response_text})
    except Exception as e:
        print(e)
        from traceback import print_exc
        print_exc()
        response = requests.get("http://localhost:5000/parse", params={"q": request.form["text"]}).json()
        print(type(response['intent']))
        return jsonify({"status": "success", "response": str(response["intent"])})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8000)
