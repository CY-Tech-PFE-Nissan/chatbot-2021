import requests
import json
# requete sur le port 8083 : code avatar


def api_call(endpoint="autonomie",vin_user="VF1AG000X64744477"):
	url='http://dev.smartevlab.fr:8083/'+endpoint
	headers = {'vin_user':vin_user}
	payload={}
	print(url," : ", vin_user)
	response = requests.request("GET", url, headers=headers, data=payload)

	response1 = json.loads(response.text)

	return response1
