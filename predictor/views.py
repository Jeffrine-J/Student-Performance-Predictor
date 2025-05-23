from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import StudentDataForm
import joblib
import os

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'predictor/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'predictor/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    prediction = None
    if request.method == 'POST':
        form = StudentDataForm(request.POST)
        if form.is_valid():
            data = [
                form.cleaned_data['math_score'],
                form.cleaned_data['reading_score'],
                form.cleaned_data['writing_score'],
                form.cleaned_data['attendance'],
                form.cleaned_data['study_hours'],
            ]
            model_path = os.path.join('predictor', 'ml_model', 'model.pkl')
            model = joblib.load(model_path)
            pred = model.predict([data])[0]
            prediction = "Pass" if pred == 1 else "Fail"
            return render(request, 'predictor/result.html', {'prediction': prediction, 'data': data})
    else:
        form = StudentDataForm()
    return render(request, 'predictor/home.html', {'form': form})

@login_required
def dashboard_view(request):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import io
    import urllib, base64
    import pandas as pd

    df = pd.read_csv('StudentsPerformance.csv')
    plt.figure(figsize=(6,4))
    df['math score'].hist(bins=20, color='skyblue')
    plt.title('Math Score Distribution')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    return render(request, 'predictor/dashboard.html', {'data': uri})
