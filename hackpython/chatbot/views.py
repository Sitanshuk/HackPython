from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import(authenticate,
    get_user_model,
    login,
    logout,
    )
import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .form import SignupForm,LoginForm



from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from flask import Flask
from flask import render_template, jsonify
import requests
from response import *
import random
from fuzzywuzzy import process
from django.views.decorators.csrf import csrf_exempt
import json

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
            if mandatory_string in request.POST["text"]:
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


get_random_response = lambda intent: random.choice(response[intent])
isClosingCard = False
chequeBookAddress = 0


# @app.route('/chat', methods=["POST"])
@csrf_exempt
def chat(request):
    if request.method == 'POST':
            start = form.cleaned_data.get('text')
            print(start)

@csrf_exempt
def post_announcement(request):
    global isClosingCard
    """
    chat end point that performs NLU using rasa.ai
    and constructs response from response.py
    """
    start = None
    try:
        if request.method == 'POST':
            start = request.POST['text']   
            print(start)
    
            response2 = requests.get("http://localhost:5000/parse",params = {"q": request.POST["text"]})
            print(response2)
            # response = requests.get("http://localhost:5000/parse?q="+request.form["text"])
            response2 = response2.json()
            # print(type(response2),"tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
            intent = response2["intent"]
            intent = intent["name"]
            entities = response2["entities"]
            length = len(entities)
            if length > 0:
                entity = entities[0]["entity"]
                value = entities[0]["value"]
            else:
                entity, value = None, None
            if intent == "event-request":
                response_text = get_event(entities["day"], entities["time"], entities["place"])
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
                # rishab = json.loads('{"status": "success", "response": "Enter your address: "}')
                _response = JsonResponse({"status": "success", "response": "Enter your address: "})
                chequeBookAddress = chequeBookAddress + (1 << 1)
                return _response
                # return rishab
            elif chequeBookAddress == 3:

                if len(request.POST['text']) > 5:
                    chequeBookAddress = 0
                    a = {
                    "status": "success",
                    "response": "Cheque book will be delivered to your address: \n{}.\nNomial fees will be deducted from your bank account.".format(request.POST['text'])
                    }
                    # rishab = json.loads(str(a))
                    return JsonResponse({"status": "success",
                                    "response": "Cheque book will be delivered to your address: \n{}."
                                                "\nNomial fees will be deducted from your bank account.".format(
                                        request.POST['text'])})
                else:
                    # rishab = json.loads('{"status": "success", "response": "Please enter a valid address."}')
                    return JsonResponse({"status": "success", "response": "Please enter a valid address."})
                return rishab
            else:
                # rishab = json.loads('{"status": "success", "response": {}}'.format(response_text))
                # return rishab
                return JsonResponse({"status": "success", "response": response_text})

    except Exception as e:
        print(e)
        from traceback import print_exc
        print_exc()
        response2 = requests.get("http://localhost:5000/parse",params ={"q": request.POST["text"]}).json()
        print(type(response2['intent']))
        # rishab = json.loads('{"status": "success", "response": {}}'.format(str(response2["intent"])))
        # return rishab
        return JsonResponse({"status": "success", "response": str(response2["intent"])})

    return render(request,"index.html",{"start":start})


def error(request):
    context_data={
        #,
    }
    return render(request,"error.html",context_data)

def post_forgotpassword(request):
    return render(request,"forgotpassword.html",{})

def post_logout(request):
    logout(request)
    return redirect("/chatbot/home/")       

def post_login(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username = email, password = password)
            if user is not None:
                login(request,user)
                return redirect('/announcement/home/')
            else:
                message = "Invalid Email id or Password. Please Try Again!!"
                return render(request,"login.html",{'form':form,'message':message})

    else:
        form = LoginForm()
    return render(request,"login.html",{'form':form})

def post_register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            to_email = form.cleaned_data.get('email')
            user.username = to_email
            user_list=User.objects.all()
            for query in user_list:
                if user.username in query.username:
                    error = "Email Already Exists . "
                    return render(request, 'register.html', {'form': form,'error':error})
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('account_activation_email.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages = 'Please confirm your email address to complete the registration'
            return render(request, 'register.html', {'form': form,'message':messages})
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/chatbot/home/')
    else:
        return HttpResponse('Activation link is invalid!')


def dashboard(request):
    return render(request,"dashboard.html",{})      

def eduloans(request):
    return render(request,"eduloan.html",{})

def personalloans(request):
    return render(request,"Personal Loan.html",{})

def homeloans(request):
    return render(request,"homeloan.html",{})

def deposit(request):
    return render(request,"deposit.html",{})        

def savings(request):
    return render(request,"savingsacc.html",{})

def current(request):
    return render(request,"currentacc.html",{})


def chat(request):
    return render(request,"chat.html",{})

def readmorei(request):
    return render(request,"readmorei.html",{})

def readmoref(request):
    return render(request,"readmoref.html",{})