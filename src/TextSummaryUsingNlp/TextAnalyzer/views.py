from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .forms import TextInputForm
from Helper import Helper

analysis = Helper()

# Create your views here.
def index(request):
    return HttpResponse("Hello World!")

def home(request):
    if request.method =='POST':
        form = TextInputForm(request.POST)

        if form.is_valid():
            raw_text = form.cleaned_data['text']

            # Perform text analysis using your Helper class
            summary = analysis.summarize_texts([raw_text])  # Pass a list containing the raw_text
            sentiment_result = analysis.find_sentiment([raw_text])
            emotion_result = analysis.get_emotions_detected([raw_text])  # Pass a list containing the raw_text

            analyzed_data = {
                'raw_text': raw_text,
                'summary': summary,
                'sentiment_result': sentiment_result,
                'emotion_result': emotion_result,
            }

            return render(request, 'TextAnalyzer/result.html', analyzed_data)

    else:
        initial_text_value = ""  # Set your desired initial value
        form = TextInputForm(initial={'text': initial_text_value})

    return render(request, 'TextAnalyzer/home.html', {'form': form})

def about(request):
    return render(request, 'TextAnalyzer/about.html')