from django.shortcuts import render, redirect
from .forms import ProfileRegisterForm, UserRegisterForm, PostContent
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
import pickle

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        p_form = ProfileRegisterForm(request.POST)
        if form.is_valid() and p_form.is_valid():
            user = form.save(commit=False)
            profile = p_form.save(commit=False)
            profile.user = user
            user.save()
            profile.save()
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('website/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
        else:
            return render(request,'website/register.html',{'form': form, 'p_form': p_form})
    else:
        form = UserRegisterForm()
        p_form = ProfileRegisterForm()
    return render(request,'website/register.html',{'form': form, 'p_form': p_form})

@login_required
def home(request):
    if request.method == 'POST':
        post_form = PostContent(request.POST)
        post = post_form.save(commit=False)
        loaded_model = pickle.load(open("model/emotion.pkl", 'rb'))
        print(loaded_model.predict(post.content))
        post.user = request.user
        post.save()
        return render(request,'website/home.html', {'post_form': post_form})
    else:
        post_form = PostContent()
    return render(request,'website/home.html', {'post_form': post_form})


def activate(request, uidb64, token):  
    User = get_user_model()
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  