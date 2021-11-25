# inscription d'un utilisateur dans la base de données. Si utilisateur déja inscrit, inscription refusée.

import requests
import json
#from sql_base_avatar import killeur, verification
#from sql_base_avatar import create_account
import aiohttp
import asyncio
import json
import ast
import csv
#from app_avatar import *
import sys
from .sql_base_avatar import *

#avatar
api_key_gigya = "3_4LKbCcMMcvjDm3X89LU4z4mNKYKdl_W0oD9w-Jvih21WqgJKtFZAnb9YdUgWT9_a"
api_key_kameron = 'Ae9FDWugRxZQAGm3Sxgk7uJn6Q4CGEA2'

expiration = "9000"


def get_vins(email, password):
  vin_user=" "

  url = "https://accounts.eu1.gigya.com/accounts.login?apiKey="+ api_key_gigya + "&loginID="+email+"&password="+password


  payload={}
  headers = {}

  response = requests.request("GET", url, headers=headers, data=payload)

  response1 = json.loads(response.text)
  cookie_value = response1['sessionInfo']['cookieValue']
  #print(type(cookie_value))

  url2 = "https://accounts.eu1.gigya.com/accounts.getAccountInfo?apiKey=" + api_key_gigya + "&login_token=" + cookie_value
  #print(url2)

  response = requests.request("POST", url2, headers=headers, data=payload)

  response2 = json.loads(response.text)
  personId = response2['data']['personId']
  #print(personId)

  url3 = "https://accounts.eu1.gigya.com/accounts.getJWT?ApiKey=" + api_key_gigya + "&login_token=" + cookie_value + "&fields=data.personId,data.gigyaDataCenter&expiration=" + expiration
  #print(url3)
  response = requests.request("GET", url3, headers=headers, data=payload)

  response3 = json.loads(response.text)
  id_token = response3['id_token']
  #print(id_token)

  url4 = "https://api-wired-prod-1-euw1.wrd-aws.com/commerce/v1/persons/" + personId + "?country=FR"
  #print(url4)
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
  #print(url5)

  headers = {
    'x-gigya-id_token': id_token,
    'apikey': api_key_kameron
  }

  response = requests.request("GET", url5, headers=headers, data=payload)
  response5 = json.loads(response.text)


  url6 = "https://api-wired-prod-1-euw1.wrd-aws.com/commerce/v1/accounts/" + accountId + "/vehicles/" + "?country=FR"
  print(url6)

  headers = {
    'x-gigya-id_token': id_token,
    'apikey': api_key_kameron
  }

  response = requests.request("GET", url6, headers=headers, data=payload)
  response6 = json.loads(response.text)
  print(response6)
  #vin1=response5['data']['vehicleLinks'][5]['vin']


  print("quel véhicule souhaitez vous utiliser ?" )
  #création de 2 dictionnaires avec un système "clés" "valeurs" afin de récupérer le modelcode et urlcar associé au vin du véhicule que l'utilisateur choisira
  vin_modelcode= {}
  vin_urlcar={}
  #création d'un dictionnaire au format suivant :chaque clé est un vin et chaque valeur est un dico contenant le model et l'url du vin. Exemple:  
  #{
  #  le_vin:{
  #    'vin_modelcode':le_model
  #    'vin_urlcar':l_url
  #  }
  #}
  dico = {}
  for elem in response6['vehicleLinks']:
      url_car = elem['vehicleDetails']['assets'][0]['renditions'][0]['url']
      model_code = elem['vehicleDetails']['model']['code']
      vin = elem['vin']

      dico[vin] = {}
      dico[vin]['model_code'] = model_code
      dico[vin]['url_car'] = url_car

      vin_modelcode[vin]=model_code #Pour chaque véhicule disponible, on ajoute dans le dict. le vin (clé) asscié au modelcode (valeur)
      vin_urlcar[vin]=url_car #Pour chaque véhicule disponible, on ajoute dans le dict. le vin (clé) associé à l'urlcar (valeur)
      print(vin + "   voir photo véhicule en cliquant sur le lien : " + url_car + '\n') #on affiche une liste des vin dispo ainsi que l'urlcar associé afin de voir l'image du véhicule
      #print(vin) 
      #print(i, response5['data']['vehicleLinks'][i]['vin'])

  return dico

def new_vin_db_input(vin,dico):

  #choix du modèle par l'utilisateur:
  #vin_user = input ("entrez le vin du véhicule que vous voulez: ") #on recupere l'entrée clavier du terminal afin de faire des test (à modifier lorsque Corentin et Ryan auront mis en place l'IHM)
  modelCodeVehicule = vin_modelcode[vin_user] 
  urlVehicule= vin_urlcar[vin_user]
  if verification(vin_user) == False: #si véhicule pas encore inscrit dans la base de données, on ajoute le véhicule à celle ci
    create_account(vin_user,email,password) 
    modification_type(vin_user,"Model",modelCodeVehicule) #ajout dans la base de données du modelcode
    modification_type(vin_user,"url_car",urlVehicule) #ajout dans la base de données de l'urlcar
    print("utilisateur inscrit dans la base de données")
  else:#si véhicule déja inscrit, on ne recrée pas de compte pour éviter doublons
    print("ce véhicule est deja inscrit dans la base de donnée")

