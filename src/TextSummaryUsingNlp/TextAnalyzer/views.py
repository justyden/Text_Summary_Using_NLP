from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .forms import TextInputForm

# Create your views here.
def index(request):
    return HttpResponse("Hello World!")

def home(request):
    if request.method =='POST':
        form = TextInputForm(request.POST)

        if form.is_valid():
            # CODE FOR TEXT ANALYSIS WILL GO HERE

            raw_text = form.cleaned_data['text']
            analyzed_data: dict = {'sentiment_analysis': 10, 'emotion_analysis': 'happy'}    # what ever analysis is performed, package it into here
            return render(request, 'TextAnalyzer/result.html', analyzed_data)

    else:
        initial_text_value = ""  # Set your desired initial value
        form = TextInputForm(initial={'text': initial_text_value})

    return render(request, 'TextAnalyzer/home.html', {'form': form})



