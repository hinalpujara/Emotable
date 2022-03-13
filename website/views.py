from django.shortcuts import render, redirect
from .forms import ProfileRegisterForm, UserRegisterForm

# Create your views here.
def welcome(request):
    return render(request,'website/welcome.html')

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
            return redirect('home')
        else:
            return render(request,'website/register.html',{'form': form, 'p_form': p_form})
    else:
        form = UserRegisterForm()
        p_form = ProfileRegisterForm()
    return render(request,'website/register.html',{'form': form, 'p_form': p_form})