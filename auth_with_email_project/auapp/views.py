from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from random import randrange
from auth_with_email_project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

def usignup(request):
	if request.method == "POST":
		un = request.POST.get('un')
		em = request.POST.get('em')
		try:
			usr = User.objects.get(username=un)
			return render(request, 'usignup.html', {'msg':'username already registered'})
		except User.DoesNotExist:
			try:
				usr = User.objects.get(email=em)
				return render(request, 'usignup.html', {'msg':'email already registered'})
			except User.DoesNotExist:
				pw = ""
				text = "123456789"
				for i in range(6):
					pw = pw + text[randrange(len(text))]
				print(pw)
				subject = "welcome"
				msg = "ur password is " + str(pw)
				send_mail(subject, msg, EMAIL_HOST_USER, [em])
				usr = User.objects.create_user(username=un,password=pw,email=em)
				usr.save()
				return redirect('ulogin')
		else:
			return  render(request, 'usignup.html')

def ulogin(request):
	if request.method == "POST":
		un = request.POST.get('un')
		pw = request.POST.get('pw')
		usr = authenticate(username=un, password=pw)
		if usr is None:
			return render(request, 'ulogin.html', {'msg':'invalid credentials'})
		else:
			login(request,usr)
			return redirect('home')
	else:
		return render(request,'ulogin.html')

def ulogout(request):
	logout(request)
	return redirect('ulogin')