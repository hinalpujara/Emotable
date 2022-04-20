import email
from multiprocessing import context
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import ProfileRegisterForm, UserRegisterForm, PostContent
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from .models import Like, Post,Comment, Profile
from .forms import UserLoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.views import generic

# Create your views here.
emotions = ['neutral','worry','happiness','sadness','love','surprise','fun','relief','hate','empty','enthusiasm','boredom','anger']
emotions.sort()


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            p_form = ProfileRegisterForm(request.POST)
            if form.is_valid() and p_form.is_valid():
                user = form.save(commit=False)
                profile = p_form.save(commit=False)
                profile.user = user
                user.is_active = False
                user.save()
                profile.save()
                current_site = get_current_site(request)  
                mail_subject = 'Activation link'  
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
                return render(request,'website/register.html',{'form': form, 'p_form': p_form, 'modal': True}) 
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
        # loaded_model = pickle.load(open("model/emotion.pkl", 'rb'))
        # post.emotion = loaded_model.predict(post.content)
        post.emotion = "Happy"
        post.user = request.user
        post.save()
        return render(request,'website/home.html', {'post_form': post_form,'emotions':emotions})
    else:
        posts_list = Post.objects.all().order_by('-time_posted')
        post_form = PostContent()
        return render(request,'website/home.html', {'post_form': post_form, 'posts_list':posts_list,'emotions':emotions})


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
        # posts_list = Post.objects.all().order_by('-time_posted')
        # post_form = PostContent()
        # return render(request,'website/home.html', {'post_form': post_form, 'posts_list':posts_list})
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # messages.add_message(request, messages.SUCCESS, 'account activated successfully')
        # return redirect("website/welcome") 
    else:  
        return HttpResponse('Activation link is invalid!')  

def search(request):
    if request.method == 'POST':
        return

def authRegister(request):
    return redirect('register')

def googleRegister(request):
    return HttpResponse('Hola')  

@login_required
def edit_prof(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form = p_form.save()
            messages.success(request, 'Profile details updated.')
            return redirect('edit-profile')
    else:
        form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'form' : form,
        'p_form' : p_form
    }
    
    return render(request, 'website/editProfile.html' ,context)

@login_required
def likePost(request,pk):
    if request.POST.get('action') == '':
        post = Post(pk=pk)
        like = Like(user=request.user,post=post)
        like.save()
        return redirect('home')
    else:
        return redirect('home')

@login_required
def unlikePost(request,pk):
    if request.POST.get('action') == '':
        user = request.user
        post = Post.objects.get(pk=pk)
        post.like_set.filter(user=user).delete()
        return redirect('home')
    else:
        return redirect('home')

@login_required
def postComment(request):
    if request.POST.get('action') == '':
        user = request.user
        comment = request.POST.get('comment')
        post_id = request.POST.get('post_id')
        post = Post(pk=post_id)
        post_comment = Comment(user=user,post=post,content=comment)
        # post_comment.save()
        return HttpResponse(status=204)
    else:
        return redirect('home')
