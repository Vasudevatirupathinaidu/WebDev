from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile, Skill, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles

def loginUser(request):
    page = "login"
    if request.user.is_authenticated:   
        return redirect("profiles")
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = Profile.objects.get(username=username)    
        except:
            messages.error(request, 'Username does not exist!')
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in!')
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')
            else:
                messages.error(request, "Username or Password is incorrect!")
    context = {"page": page}
    return render(request, "users/login-register.html", context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'You have successfully logged out!')
    return redirect("login")

def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have successfully registered!')
            login(request, user)

            return redirect("edit-account")

        else:
            messages.error(request, 'An error has occured during registration!')

    context = {"page": page, "form": form}
    return render(request, 'users/login-register.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)
    context = {"profiles": profiles, "search_query": search_query, "custom_range": custom_range}
    return render(request, "users/profiles.html", context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    mainSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description__exact="")
    context = {"profile": profile, "mainSkills": mainSkills, "otherSkills": otherSkills}
    return render(request, "users/user-profile.html", context)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, 'users/account.html', context)

@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congrats! You have updated the account.')
            return redirect("account")
    context = {"form": form}
    return render(request, 'users/profile-form.html', context)


@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect("account")
    context={"form": form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was updated!')
            return redirect("account")
    context = {"form": form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect("account")
    context = {"object": skill}
    return render(request, 'delete-template.html', context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_messages = message_requests.filter(is_read=False).count()
    context = {"messages": message_requests, "unread_messages": unread_messages}
    return render(request, 'users/inbox.html', context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Your message was successfully sent!")
            return redirect('profile', pk=recipient.id)

    context = {"recipient": recipient, "form": form}
    return render(request, 'users/message-form.html', context)