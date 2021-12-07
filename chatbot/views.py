from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import default_storage
from pathlib import Path
from django.shortcuts import redirect, render



import json
import csv
import requests

from .avatar_db_requests.creation_account import new_account
from .chatbot import Chatbot
from .features.icon_recognition import get_prediction
from .features.air_filter import get_analysis
from .features.voice_interactions import get_text_from_audio
from .features.voice_interactions import get_audio_from_text
from .features.voice_interactions import remove_audios
from .avatar_endpoints.TestAutonomie import api_call


SENTIMENT_ANALYSIS_FOLDER = (
    Path(__file__).resolve().parent / "features" / "sentiment_analysis"
)

MODEL_PATH = str(SENTIMENT_ANALYSIS_FOLDER / "models")

UPLOAD_FOLDER = Path(__file__).resolve().parent.parent / "static" / "uploads"


# FIXME: create a Chatbot instance associated to an user session
custom_chatbot = Chatbot(rule_file="rules.json", sa_model_path=MODEL_PATH)


def index(request):
    return render(request, "chatbot/index.html")


def chat(request):
    if 'vin' in request.session.keys():
        return render(request, "chatbot/chat.html")
    return redirect("/chatbot/api_auth")


def api_auth(request):
    context={}
    return render(request, "chatbot/api_auth.html",context)

def cars(request):
    return render(request, "chatbot/cars.html")
    

def check_user(request):
    """Try to login user with its credentials

    Parameter
    ---------
    request: Request (method)
    Returns
    ---------
    response: HttpResponse
    """

    if request.method == "POST":
        email = 	request.POST.get('login','')
        password = 	request.POST.get('password','')
        api_key_gigya = "3_4LKbCcMMcvjDm3X89LU4z4mNKYKdl_W0oD9w-Jvih21WqgJKtFZAnb9YdUgWT9_a"
        api_key_kameron = "Ae9FDWugRxZQAGm3Sxgk7uJn6Q4CGEA2"

        expiration = "9000"

        #email = "smylet51@gmail.com"
        #password = "TestRenault123"

        url = "https://accounts.eu1.gigya.com/accounts.login?apiKey=3_4LKbCcMMcvjDm3X89LU4z4mNKYKdl_W0oD9w-Jvih21WqgJKtFZAnb9YdUgWT9_a&loginID="+email+"&password="+password

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        response1 = json.loads(response.text)

        try :
            cookie_value = response1['sessionInfo']['cookieValue']
            #print(type(cookie_value))

            url2 = "https://accounts.eu1.gigya.com/accounts.getAccountInfo?apiKey=" + api_key_gigya + "&login_token=" + cookie_value

            response = requests.request("POST", url2, headers=headers, data=payload)

            response2 = json.loads(response.text)
            personId = response2['data']['personId']
            #print(personId)
            url3 = "https://accounts.eu1.gigya.com/accounts.getJWT?ApiKey=" + api_key_gigya + "&login_token=" + cookie_value + "&fields=data.personId,data.gigyaDataCenter&expiration=" + expiration

            response = requests.request("GET", url3, headers=headers, data=payload)

            response3 = json.loads(response.text)
            id_token = response3['id_token']
            #print(id_token)

            url4 = "https://api-wired-prod-1-euw1.wrd-aws.com/commerce/v1/persons/" + personId + "?country=FR"

            headers = {
            'x-gigya-id_token': id_token,
            'apikey': api_key_kameron
            }

            response = requests.request("GET", url4, headers=headers, data=payload)

            response4 = json.loads(response.text)
            
            for i in range(len(response4['accounts'])):
                #print(response4['accounts'][i])
                if response4['accounts'][i]['accountType'] == 'MYRENAULT':
                    accountId = response4['accounts'][i]['accountId']
            #print(accountId)

            url5 = "https://api-wired-prod-1-euw1.wrd-aws.com/commerce/v1/accounts/" + accountId + "?country=FR"

            headers = {
            'x-gigya-id_token': id_token,
            'apikey': api_key_kameron
            }

            response = requests.request("GET", url5, headers=headers, data=payload)
            response5 = json.loads(response.text)
            vin1=response5['data']['vehicleLinks'][0]['vin']
            #vin2=response5['data']['vehicleLinks'][1]['vin']
            print(vin1)
            #print(type(vin1))

            url6 = "https://api-wired-prod-1-euw1.wrd-aws.com/commerce/v1/accounts/"+accountId+"/kamereon/kca/car-adapter/v2/cars/"+vin1+"/battery-status?country=FR"



            headers = {
            'x-gigya-id_token': id_token,
            'apikey': api_key_kameron
            }
            response = requests.request("GET", url6, headers=headers, data=payload)
            response6 = json.loads(response.text)

            url7 = "https://api-wired-prod-1-euw1.wrd-aws.com/commerce/v1/accounts/" + accountId + "/vehicles/" + "?country=FR"

            response = requests.request("GET", url7, headers=headers, data=payload)
            response7 = json.loads(response.text)
            request.session['vim'] = response7
            request.session['email'] = email
            request.session['password'] = password
            print("c'est bon")
            return redirect("/chatbot/cars")

        except KeyError as e:
            print("c'est pas bon")
            return redirect("/chatbot/api_auth")

def create_account(request):  
    if request.method == "POST":
        data = json.load(request)['vin']
        #new_account(request.session['email'],request.session['password'],data)
        request.session["vin"] = data
    return HttpResponse(request)

def discuss(request):
    """Receives a message and generates an answer with
    a text message, an audio message and an optional video

    Parameter
    ---------
    request: Request (method, "input")
    Returns
    ---------
    response: JsonResponse ('message', 'titles')
    """
    if request.method == "POST":
        # Get user input
        data = json.load(request)["input"]

        # Computer answer / video title if existing
        message, video = custom_chatbot(data)
        messages = message.split("@nl")  # Split paragraphs

        # Look if order message needs an api call
        messages = [message if message.split(' ')[0]!='order' else api_call(message.split(' ')[1],request.session['vin']) for message in messages]

        # Create audios
        titles = []
        for i in range(len(messages)):
            title = messages[i].split(" ")[0]
            titles.append(title)
            get_audio_from_text(
                messages[i], str(UPLOAD_FOLDER) + "/audios/" + title + ".mp3"
            )

        # Create videos
        #if len(video) > 0:
        #    videos = video.split("@nl")
        #else:
        videos = []

        response = JsonResponse(
            {"message": messages, "titles": titles, "videos": videos}
        )
        return response
    return JsonResponse({"message": "Nothing submitted"})


def upload_file(request):
    """Uploads a file (picture) to the UPLOAD_FOLDER

    Parameter
    ---------
    request: Request (method, "uploadFile")
    Returns
    ---------
    response: JsonResponse ('message', 'path')
    """
    if request.method == "POST":
        if "uploadFile" not in request.FILES:
            return JsonResponse({"message": "uploadFile not in request.FILES"})
        file = request.FILES.get("uploadFile")
        if file.name == "":
            return JsonResponse({"message": "No selected file"})
        if file:
            filename = "".join(file.name.split(":"))
            original_path = UPLOAD_FOLDER / filename
            path = default_storage.save(original_path, file)
            return JsonResponse({"path": str(path)})
    return JsonResponse({"message": "Nothing submitted"})


def icon_recognition(request):
    """Receives a path and makes prediction on icons out of it

    Parameter
    ---------
    request: Request (method, "path")
    Returns
    ---------
    response: JsonResponse ('message', 'description')
    """
    if request.method == "POST":
        # Get data and make prediction
        path = json.load(request)["path"]
        input_img = open(path, "rb")
        img_bytes = input_img.read()
        response = get_prediction(img_bytes=img_bytes)
        # Find description based on the response
        description = ""
        with open("chatbot/data/image_description.csv", newline="") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            for row in reader:
                if row[0] == response:
                    description = row[1]
                    break
        return JsonResponse({"message": response, "description": description})
    return JsonResponse({"message": "Nothing submitted"})


def air_filter_analysis(request):
    """Receives a path and makes prediction on air filter out of it

    Parameter
    ---------
    request: Request (method, "path")
    Returns
    ---------
    response: JsonResponse ('message')
    """
    if request.method == "POST":
        # Get data, convert image to bytes and predict
        path = json.load(request)["path"]
        input_img = open(path, "rb")
        img_bytes = input_img.read()
        response = get_analysis(img_bytes=img_bytes)
        return JsonResponse({"message": response})
    return JsonResponse({"message": "Nothing submitted"})


def speech_to_text(request):
    """Receives an audio file and converts it to text

    Parameter
    ---------
    request: Request (method, "uploadAudio")
    Returns
    ---------
    response: JsonResponse ('message')
    """
    if request.method == "POST":
        if "uploadAudio" not in request.FILES:
            return JsonResponse({"message": "uploadAudio not in request.FILES"})
        file = request.FILES.get("uploadAudio")
        if file.name == "":
            return JsonResponse({"message": "No selected file"})
        if file:
            filename = "".join(file.name.split(":"))
            original_path = UPLOAD_FOLDER / "audios" / filename
            path = default_storage.save(original_path, file)
            response = get_text_from_audio(str(path))
            return JsonResponse({"message": response})
    return JsonResponse({"message": "Nothing submitted"})


def remove(request):
    """Removes all the audio files to prevent bugs

    Parameter
    ---------
    request: Request (method)
    Returns
    ---------
    response: HttpResponse
    """
    if request.method == "GET":
        remove_audios()
        return HttpResponse(
            "Audio files correctly removed", content_type="text/plain"
        )
    return HttpResponse("remove_audios : Wrong method used")
