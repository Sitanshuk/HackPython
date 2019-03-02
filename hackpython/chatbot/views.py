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



from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response


def post_announcement(request):
	return render(request,"index.html",{})


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