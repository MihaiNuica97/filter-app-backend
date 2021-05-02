from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from django.shortcuts import render

nltk.data.path.append("/home/nltk_data")

def hello(request):
    print("Handling request to home page.")
    return HttpResponse("Hello, Azure!")


@csrf_exempt
def filter_this(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)  # request.raw_post_data w/ Django < 1.4
        data = word_tokenize(json_data['content'])
        print(data)
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("You tried a GET instead of a POST")