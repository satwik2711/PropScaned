from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, BrokerSerializer, OwnerSerializer, BuyerSerializer
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import credentials, auth
from django.http import JsonResponse
from accounts.models import PropScanUser
from django.db.utils import IntegrityError
from .models import *
import boto3
import os
import uuid
from django.http import QueryDict
import json
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from property_listing.models import *
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


@api_view(['POST'])
def nearby_experts(request):
    location = request.data.get('location')
    distance = request.data.get('distance')

    brokers = Broker.objects.all()

    serialized_brokers = []
    for broker in brokers:
        city = broker.city

        if location and distance:
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
            params = {
                'origins': location,
                'destinations': city,
                'key': 'AIzaSyCzkfZU5H2EfmRZdzubLoVas9t8E32uroU'
            }
            response = requests.get(url, params=params)
            distance_result = response.json()

            rows = distance_result.get('rows')
            if rows and len(rows) > 0:
                elements = rows[0].get('elements')
                if elements and len(elements) > 0:
                    distance_info = elements[0].get('distance')
                    if distance_info:
                        distance_value = distance_info.get('value')
                    else:
                        distance_value = None
                else:
                    distance_value = None
            else:
                distance_value = None

            if distance_value is not None and distance_value < distance:
                serialized_broker = BrokerSerializer(broker).data
                serialized_broker['distance'] = distance_value
                serialized_brokers.append(serialized_broker)
        else:
            serialized_broker = BrokerSerializer(broker).data
            serialized_broker['distance'] = None
            serialized_brokers.append(serialized_broker)

    return Response(serialized_brokers)




# Initialize Firebase Admin SDK
cred = credentials.Certificate('propscan-7362e-firebase-adminsdk-4f0fb-864431e695.json')  # Replace with your own service account key file
firebase_admin.initialize_app(cred)

def send_otp(phone_number):
            api_key='9b332561-2bbc-11ee-addf-0200cd936042'
            url=f'https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/AUTOGEN3/'
            # url = f'https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}'
            try:
                res = requests.get(url)
                res.raise_for_status()
                return True
            except requests.exceptions.HTTPError as e:
                return False
            except Exception as e:
                return False
    

def verify_otp(phone_number,otp):
    api_key='9b332561-2bbc-11ee-addf-0200cd936042'
    url=f'https://2factor.in/API/V1/{api_key}/SMS/VERIFY3/{phone_number}/{otp}'
    try:
        res = requests.get(url)
        #check if the response is status 200
        print(res.text)
        response_json = res.json()
        print(response_json["Status"])
        if response_json["Status"] == "Success":
            return True
        else:
            return False
    except:
        print("except failure block")
        return False


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
       
        
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        otp = data.get('otp')
        print("---------")
        print(phone_number)
        print(PropScanUser.objects.filter(phone_no=phone_number).exists())

        # Check if the phone number exists in Firebase Authentication
        # try:
        #     user = auth.get_user_by_phone_number(phone_number)
        # except firebase_admin.auth.UserNotFoundError:
        #     return JsonResponse({'status': 'user does not exist'})

        if PropScanUser.objects.filter(phone_no=phone_number).exists():
            user = PropScanUser.objects.filter(phone_no=phone_number).first()
            user_id = user.id
            if otp:
                # Verify the OTP
                if verify_otp(phone_number,otp):
                    user = PropScanUser.objects.filter(phone_no=phone_number)
                    token = RefreshToken.for_user(user) 
                    return JsonResponse({'user_id': user_id, 'message': 'Login successful','token': str(token.access_token)})
                else:
                    return JsonResponse({'message': 'Invalid OTP.'}, status=400)
            else:
                # Send OTP to the user's phone number
                if send_otp(phone_number):
                    return JsonResponse({'message': 'OTP sent successfully.'})
                else:
                    return JsonResponse({'message': 'Failed to send OTP.'}, status=500)
        else:
            return JsonResponse({'message': 'User does not exist.'}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    user_data = request.data.get('user')  # Parse 'user' JSON from request.data
    user_type = user_data.get('user_type', '')
    User = PropScanUser

    data = {k: v[0] for k, v in dict(request.POST).items()}
    data['user'] = user_data  # Replace 'user' string with parsed data

    if user_type == User.BUYER:
        serializer = BuyerSerializer(data=data)
    elif user_type == User.BROKER:
        serializer = BrokerSerializer(data=data)
    elif user_type == User.OWNER:
        serializer = OwnerSerializer(data=data)
    else:
        return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)
    

    if serializer.is_valid():
        main_image = request.FILES.get('main_image')
        s3 = boto3.client('s3', aws_access_key_id=os.environ['KEY_ID'], aws_secret_access_key=os.environ['ACCESS_KEY'])
        bucket = 'propscan.s00'
        if main_image:
            unique_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(main_image.name)[1]
            filename = f"uploads/broker_pfp/{unique_filename}{file_extension}"

            try:
                s3.upload_fileobj(Fileobj=main_image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                serializer.validated_data['main_image_link'] = file_url
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            serializer.save()
            return Response({
                'message': 'Signup successful',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({
                'error': 'A user with this email already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def get_buyer(request):
    buyer = Buyer.objects.all()
    serializer = BuyerSerializer(buyer, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_owner(request):
    owner = Owner.objects.all()
    serializer = OwnerSerializer(owner, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def get_broker(request):
    broker = Broker.objects.all()
    serializer = BrokerSerializer(broker, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete(request, pk):
    try:
        user = PropScanUser.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except PropScanUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_buyer(request, pk):
    try:
        buyer = Buyer.objects.get(user__pk=pk)
    except Buyer.DoesNotExist:
        return Response({"error": "Buyer not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = BuyerSerializer(buyer, data=request.data, partial=True)  # set partial=True to update data partially
    if serializer.is_valid():
        # Update buyer data here if needed
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({"error": "Error occurred while saving the buyer"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_owner(request, pk):
    try:
        owner = Owner.objects.get(user__pk=pk)
    except Owner.DoesNotExist:
        return Response({"error": "Owner not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OwnerSerializer(owner, data=request.data, partial=True)  # set partial=True to update data partially
    if serializer.is_valid():
        # Update owner data here if needed
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({"error": "Error occurred while saving the owner"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_broker(request, pk):
    try:
        broker = Broker.objects.get(user__pk=pk)
    except Broker.DoesNotExist:
        return Response({"error": "Broker not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = BrokerSerializer(broker, data=request.data, partial=True)  # set partial=True to update data partially
    if serializer.is_valid():
        # Update broker data here if needed

        main_image = request.FILES.get('main_image')
        if main_image:
            s3 = boto3.client('s3', aws_access_key_id=os.environ['KEY_ID'], aws_secret_access_key=os.environ['ACCESS_KEY'])
            bucket = 'propscan.s00'
            unique_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(main_image.name)[1]
            filename = f"uploads/broker_images/{unique_filename}{file_extension}"

            try:
                s3.upload_fileobj(Fileobj=main_image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                serializer.validated_data['main_image_link'] = file_url
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#FAV

@api_view(['POST'])
def add_favorite_type1(request, user_id, property_id):
    # get the user
    user = get_object_or_404(PropScanUser, id=user_id)

    # get the property
    property = get_object_or_404(PropertyType1, id=property_id)

    # add the property to the user's favorites
    user.favorites_type1.add(property)

    return Response({"message": "Property added to favorites"}, status=status.HTTP_200_OK)



@api_view(['POST'])
def add_favorite_type2(request, user_id, property_id):
    # get the user
    user = get_object_or_404(PropScanUser, id=user_id)

    # get the property
    property = get_object_or_404(PropertyType2, id=property_id)

    # add the property to the user's favorites
    user.favorites_type2.add(property)

    return Response({"message": "Property added to favorites"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_favorite_type3(request, user_id, property_id):
    # get the user
    user = get_object_or_404(PropScanUser, id=user_id)

    # get the property
    property = get_object_or_404(PropertyType3, id=property_id)

    # add the property to the user's favorites
    user.favorites_type3.add(property)

    return Response({"message": "Property added to favorites"}, status=status.HTTP_200_OK)






