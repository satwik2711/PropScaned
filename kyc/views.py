from django.shortcuts import render
import requests
import json
#import jsonresponse
from django.http import JsonResponse
#import csrf exempt
from django.views.decorators.csrf import csrf_exempt
#django api which takes the aadhar number requests

#add csrf exempt decorator

# @csrf_exempt
# def auth_token(request):
#     if request.method=='GET':
#         url = "https://api.sandbox.co.in/authenticate"

#         payload = {}
#         headers = {
#         'x-api-key': 'key_live_Bk7Zp0lL12PUIGOTXyiq1qaydB6phF4f',
#         'x-api-secret': 'secret_live_qV3TNtatabj7Z1juhx4Y2FijZGe666KE',
#         'x-api-version': '1.0'
#         }
#         data = requests.request("POST", url, headers=headers, data=payload)
#         if 'auth_token' in data.get('data', {}):
#             auth_token = data['data']['auth_token']
          
#             return JsonResponse({'auth_token': auth_token})
#         return JsonResponse(response.json())

@csrf_exempt
def aadharkyc(request):
    if request.method == 'POST':
            aadhar=request.POST.get('aadhar')
            url = "https://api.sandbox.co.in/authenticate"

            payload = {}
            headers = {
            'x-api-key': 'key_live_Bk7Zp0lL12PUIGOTXyiq1qaydB6phF4f',
            'x-api-secret': 'secret_live_qV3TNtatabj7Z1juhx4Y2FijZGe666KE',
            'x-api-version': '1.0'
            }
            data = requests.request("POST", url, headers=headers, data=payload)
            if 'auth_token' in data.get('data', {}):
                auth_token = data['data']['auth_token']
            # auth_token=request.POST.get('auth_token')
            url = "https://api.sandbox.co.in/kyc/aadhaar/okyc/otp"
            payload = json.dumps({
                "aadhaar_number": "728483923967"
                })
            headers = {
            'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJhdWQiOiJBUEkiLCJyZWZyZXNoX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpVeE1pSjkuZXlKaGRXUWlPaUpCVUVraUxDSnpkV0lpT2lKd2NtOXdjMk5oYmk1a1pYWkFaMjFoYVd3dVkyOXRJaXdpWVhCcFgydGxlU0k2SW10bGVWOXNhWFpsWDBKck4xcHdNR3hNTVRKUVZVbEhUMVJZZVdseE1YRmhlV1JDTm5Cb1JqUm1JaXdpYVhOeklqb2lZWEJwTG5OaGJtUmliM2d1WTI4dWFXNGlMQ0psZUhBaU9qRTNNVGc0TURrd056UXNJbWx1ZEdWdWRDSTZJbEpGUmxKRlUwaGZWRTlMUlU0aUxDSnBZWFFpT2pFMk9EY3hPRFkyTnpSOS56dEdralZjUk9zMlNvazRKR2pEc3VOYU1MeUUxTURDeGVrWWRIc1VtamtaV2FJQktwR1A1bTJIaTM2R01kSlFvNEItUlA3aGNkRmtsaTV4LS1XeFFRdyIsInN1YiI6InByb3BzY2FuLmRldkBnbWFpbC5jb20iLCJhcGlfa2V5Ijoia2V5X2xpdmVfQms3WnAwbEwxMlBVSUdPVFh5aXExcWF5ZEI2cGhGNGYiLCJpc3MiOiJhcGkuc2FuZGJveC5jby5pbiIsImV4cCI6MTY4NzI3MzA3NCwiaW50ZW50IjoiQUNDRVNTX1RPS0VOIiwiaWF0IjoxNjg3MTg2Njc0fQ.RVz6wvxZk7L_cgeYFzQObbSzW_6lhsjs9RKOx7bmRayTpLv4jD73TYyVj0HYQF1W9C5oy688Gjk0LLUHiYMsiQ',
            'x-api-key': 'key_live_Bk7Zp0lL12PUIGOTXyiq1qaydB6phF4f',
            'x-api-version': '1.0',
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            #return response as a json response
            return JsonResponse(response.json())
    
@csrf_exempt   
def verifyaadhar(request):
    if request.method == 'POST':
        url = "https://api.sandbox.co.in/kyc/aadhaar/okyc/otp/verify"

    payload = "{\r\n  \"otp\": {{otp}},\r\n  \"ref_id\": {{ref_id}}\r\n}"
    headers = {
    'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJhdWQiOiJBUEkiLCJyZWZyZXNoX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpVeE1pSjkuZXlKaGRXUWlPaUpCVUVraUxDSnpkV0lpT2lKd2NtOXdjMk5oYmk1a1pYWkFaMjFoYVd3dVkyOXRJaXdpWVhCcFgydGxlU0k2SW10bGVWOXNhWFpsWDBKck4xcHdNR3hNTVRKUVZVbEhUMVJZZVdseE1YRmhlV1JDTm5Cb1JqUm1JaXdpYVhOeklqb2lZWEJwTG5OaGJtUmliM2d1WTI4dWFXNGlMQ0psZUhBaU9qRTNNVGc0TURrd056UXNJbWx1ZEdWdWRDSTZJbEpGUmxKRlUwaGZWRTlMUlU0aUxDSnBZWFFpT2pFMk9EY3hPRFkyTnpSOS56dEdralZjUk9zMlNvazRKR2pEc3VOYU1MeUUxTURDeGVrWWRIc1VtamtaV2FJQktwR1A1bTJIaTM2R01kSlFvNEItUlA3aGNkRmtsaTV4LS1XeFFRdyIsInN1YiI6InByb3BzY2FuLmRldkBnbWFpbC5jb20iLCJhcGlfa2V5Ijoia2V5X2xpdmVfQms3WnAwbEwxMlBVSUdPVFh5aXExcWF5ZEI2cGhGNGYiLCJpc3MiOiJhcGkuc2FuZGJveC5jby5pbiIsImV4cCI6MTY4NzI3MzA3NCwiaW50ZW50IjoiQUNDRVNTX1RPS0VOIiwiaWF0IjoxNjg3MTg2Njc0fQ.RVz6wvxZk7L_cgeYFzQObbSzW_6lhsjs9RKOx7bmRayTpLv4jD73TYyVj0HYQF1W9C5oy688Gjk0LLUHiYMsiQ',
    'x-api-key': 'key_live_Bk7Zp0lL12PUIGOTXyiq1qaydB6phF4f',
    'x-api-version': '1.0',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload) 
    
        
        

