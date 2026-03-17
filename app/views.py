from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Activity, ActivityPhoto, ActivityDocument
from .forms import ActivityForm, LoginForm, SignupForm


from django.contrib.auth.models import User

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'app/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    activities = Activity.objects.filter(user=request.user)
    # The rest of context logic remains identical, just uses the filtered activities
    recent = activities.first()
    total_activities = activities.count()
    total_teams = activities.values('team_name').distinct().count()

    all_members = set()
    for a in activities:
        for m in a.get_members_list():
            all_members.add(m.strip().lower())
    total_members = len(all_members)

    context = {
        'recent': recent,
        'total_activities': total_activities,
        'total_teams': total_teams,
        'total_members': total_members,
        'recent_activities': activities[:6],
    }
    return render(request, 'app/dashboard.html', context)


@login_required(login_url='login')
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            attachments = form.cleaned_data.get('attachments') or []
            # Photo/document creation remains the same
            for f in attachments:
                ext = f.name.split('.')[-1].lower()
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                    ActivityPhoto.objects.create(activity=activity, image=f)
                else:
                    ActivityDocument.objects.create(activity=activity, file=f)
            
            messages.success(request, 'Activity added successfully!')
            return redirect('dashboard')
    else:
        form = ActivityForm()
    return render(request, 'app/add_activity.html', {'form': form})


@login_required(login_url='login')
def activity_history(request):
    activities = Activity.objects.filter(user=request.user).prefetch_related('photos', 'documents')
    return render(request, 'app/history.html', {'activities': activities})


@login_required(login_url='login')
def activity_detail(request, pk):
    activity = get_object_or_404(Activity, user=request.user, pk=pk)
    return render(request, 'app/detail.html', {'activity': activity})


@login_required(login_url='login')
def delete_activity(request, pk):
    activity = get_object_or_404(Activity, user=request.user, pk=pk)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activity deleted.')
        return redirect('history')
    return render(request, 'app/confirm_delete.html', {'activity': activity})
