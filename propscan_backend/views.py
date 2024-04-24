from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import PropScanUser, Buyer, Owner, Broker
import random
import requests
from .settings import api_key
from rest_framework.views import APIView
from django.shortcuts import render
import json
from rest_framework.response import Response
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenError

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import TokenObtainSerializer
from .permissions import IsTokenVerified


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
@api_view(['POST'])
def generate_jwt_token(request):
    phone_no = request.data.get('phone_no', '')
    email = request.data.get('email', '')

    # Retrieve the user object based on phone number and email
    User = get_user_model()
    try:
        user = User.objects.get(phone_no=phone_no, email=email)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Generate the JWT token
    token = RefreshToken.for_user(user)

    return Response({'token': str(token.access_token)}, status=status.HTTP_201_CREATED)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import TokenError, AccessToken

@api_view(['POST'])
def verify_jwt_token(request):
    token = request.data.get('token', '')  # Extract the token from the request body

    # Verify the token
    try:
        AccessToken(token)
        return Response({'detail': 'Token is valid'}, status=status.HTTP_200_OK)
    except TokenError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class TokenObtainView(generics.CreateAPIView):
#     serializer_class = TokenObtainSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         phone_number = serializer.validated_data['phone_number']
#         email = serializer.validated_data['email']

#         # You can add your own validation logic here
#         # ...

#         token = RefreshToken.for_user(request.user)
#         return Response({'token': str(token.access_token)}, status=status.HTTP_201_CREATED)


# class TokenVerifyView(generics.GenericAPIView):
#     permission_classes = [IsTokenVerified]

#     def get(self, request, *args, **kwargs):
#         return Response({'message': 'Token is valid.'}, status=status.HTTP_200_OK)
# from django.conf import settings
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def token_verify_view(request):
#     token = request.data.get('token', '')  # Extract the token from the request body
#     try:
#         token_backend = TokenBackend(algorithm='HS256')  # Use the appropriate algorithm for your tokens
#         token_backend.decode(token, verify=True)  # Verify the token

#         # Verify the token's signature against the project's secret key
#         project_secret_key = settings.SECRET_KEY
#         token_backend.verify_token(token, project_secret_key)

#         return Response({'detail': 'Token is valid'}, status=status.HTTP_200_OK)
#     except TokenError as e:
#         return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)



# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework_simplejwt.exceptions import InvalidToken
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import CustomTokenObtainPairSerializer

# class CustomTokenObtainPairView(TokenObtainPairView):
#     print("custom api hit-----------")
#     serializer_class = CustomTokenObtainPairSerializer



# def generate_jwt_token(user):
#     print("generate token function")
#     token = AccessToken.for_user(user)
#     jwt_token = str(token)
#     return jwt_token

# def verify_jwt_token(request):
#     token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
#     try:
#         access_token = AccessToken(token)
#         user = access_token.payload.get('user_id')
#         # Perform necessary actions with the verified user
#         return JsonResponse({'user_id': user})
#     except InvalidToken:
#         return JsonResponse({'error': 'Invalid token'}, status=401)
    
    
class MyAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # Your API implementation



def homepage(request):
    current_user = request.user
    return render(request, 'index.html', {'current_user': current_user})
# otp=0
# def login(request):
    
    
#     otp=random.randint(1000,9999)
#     if request.method == 'POST':
#         if 'otp_btn' in request.POST:
#             mobile = request.POST.get('mobile')
#             exists=PropScanUser.objects.filter(phone_no=mobile).exists()
#             if exists:
#                 print(mobile)
               
#                 url = f'https://2factor.in/API/V1/{api_key}/SMS/{mobile}/{otp}'
#                 try:
#                     res = requests.get(url)
#                     res.raise_for_status()
#                     print('OTP sent successfully')
#                 except requests.exceptions.HTTPError as e:
#                     print(f'HTTP error occurred: {e}')
#                 except Exception as e:
#                     print(f'Error occurred: {e}')
#                 context = {
#                     'mobile': mobile,
#                 'otp_sent': otp
#                     }
#                 return render(request, 'login.html',context)
#             else:
#                 return HttpResponse('User does not exist')
#         if 'sub_btn' in request.POST:
#             otpp = request.POST.get('otp')
#             if otp == otpp:
#                 return HttpResponse('OTP verified successfully')
#             else:
#                 print('Invalid OTP')
#                 return HttpResponse('Invalid OTP')
                  
#     return render(request, 'login.html')


# def register_user(request):
#     if request.method=='POST':
#         form=buyer_reg(request.POST)
#         if form.is_valid():
#             user=form.cleaned_data['fullname']
#             email=form.cleaned_data['emailid']
#             user_type="BUYER"
#             phone=form.cleaned_data['phone_no']
            
#             mymodel=PropScanUser.objects.create_user(username=user,email_id=email,phone_no=phone,user_type=user_type)
            
#             buyermodel=Buyer.objects.create(phone_no=phone,full_name=user)
#             return HttpResponse('Thank you for your registration.')
#     else:
#         form=buyer_reg()
#     return render(request, 'register_user.html', {'form': form})


# def register_broker(request):
#     if request.method == 'POST':
#         form = broker_form(request.POST)
#         if form.is_valid():
#             user=form.cleaned_data['full_name']
#             email_id=form.cleaned_data['email']
#             user_type="BROKER"
#             phone=form.cleaned_data['additional_phone_no_1']
            
#             mymodel=PropScanUser.objects.create_user(username=user,email_id=email_id,phone_no=phone,user_type=user_type)
            
            
#             form.instance.user = user
#             form.save()
#             return HttpResponse('Thank you for your registration.')
#     else:
#         form = broker_form()
#     return render(request, 'register_broker.html', {'form': form})
def send_notif(request):
    #need to add registration token from database
    resgistration  = ['e1aLmMZPeegz36PP3KUw0t:APA91bGjoJBwraENbW9PHsE5IUVIh_lLhnPI99qqr_VewvRFLjbJbu_vcSfT0dk4Tu4CGbcvUfR-x8INAkqovEDuJB4OdQma2NrEPsGufjtrsizYskD_ANCpKjT5wltIAfzJkbjY0YAV']
    send_notification(resgistration , 'Code Keen added a new video' , 'Code Keen new video alert')
    return HttpResponse("sent")



    # fcm_api = "BFH1XwSjULeCn8f6NKUVqyeNUY3blyrCtjKCalcfb2p4vVA2a_e5EzP2MT022gHJR9xIOYGgd8cjY-DTWhzVDMs"
    # url = "https://fcm.googleapis.com/fcm/send"
    
    # headers = {
    # "Content-Type":"application/json",
    # "Authorization": 'key='+fcm_api
    # }

    # payload = {
    #     "registration_ids" :['e1aLmMZPeegz36PP3KUw0t:APA91bGjoJBwraENbW9PHsE5IUVIh_lLhnPI99qqr_VewvRFLjbJbu_vcSfT0dk4Tu4CGbcvUfR-x8INAkqovEDuJB4OdQma2NrEPsGufjtrsizYskD_ANCpKjT5wltIAfzJkbjY0YAV'],
    #     "priority" : "high",
    #     "notification" : {
    #         "body" : "message desc",
    #         "title" : "message_title",
    #         "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
    #         "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
            
    #     }
    # }

    # result = requests.post(url,  data=json.dumps(payload), headers=headers )
    # print(result.json())

import google.auth
from google.oauth2 import service_account
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
def _get_access_token():
  """Retrieve a valid access token that can be used to authorize requests.

  :return: Access token.
  """
  credentials = service_account.Credentials.from_service_account_file(
    'propscan-7362e-e4ac9f648631.json', scopes=SCOPES)
  request = google.auth.transport.requests.Request()
  credentials.refresh(request)
  return credentials.tokenmessaging.py

@csrf_exempt   
def send_notification(request):
    if request.method == 'POST':
        fcm_token = request.POST.get('fcm_token')
        text = request.POST.get('text')
        description = request.POST.get('description')

        if fcm_token and text and description:
            url = 'https://fcm.googleapis.com/fcm/send'
            headers = {
                        'Authorization': 'Bearer ' + _get_access_token(),
                        'Content-Type': 'application/json; UTF-8',
                    }

            data = {
                'to': fcm_token,
                'notification': {
                    'title': text,
                    'body': description,
                },
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Failed to send notification.'}, status=500)

        return JsonResponse({'error': 'Invalid parameters.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
   
   
    
    
    





def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyCbZ5pd8tS8XDWFKUaH6cQBrYZLx436Yzk",' \
         '        authDomain: "propscan-7362e.firebaseapp.com",' \
         '        databaseURL: "",' \
         '        projectId: "propscan-7362e",' \
         '        storageBucket: "propscan-7362e.appspot.com",' \
         '        messagingSenderId: "700143419070",' \
         '        appId: "1:700143419070:web:0f636a8a8916a30a7168ef",' \
         '        measurementId: "G-TR7KJRS4RW"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")



