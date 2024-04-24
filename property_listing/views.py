from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render
from .serializers import PropertyType1Serializer, PropertyType1LargeCardSerializer, PropertyType1SmallCardSerializer
from .serializers import PropertyType2Serializer, PropertyType2LargeCardSerializer, PropertyType2SmallCardSerializer
from .serializers import PropertyType3Serializer, PropertyType3LargeCardSerializer, PropertyType3SmallCardSerializer
from .serializers import PropertyType1CRMSerializer, PropertyType2CRMSerializer, PropertyType3CRMSerializer
from .models import PropertyType1, PropertyType2, PropertyType3
from rest_framework import status
from .filters import PropertyType1Filter, PropertyType2Filter, PropertyType3Filter
from django.http import JsonResponse
import googlemaps
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.views import APIView
import base64
import boto3, uuid, os
from .models import Counter
from .paginators import SmallResultsSetPagination
from rest_framework.filters import OrderingFilter

import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view

from itertools import chain
from rest_framework.response import Response
from rest_framework.decorators import api_view


#GET ALL VIEWS

@api_view(['GET'])
def get_all_properties(request):
    if request.method == 'GET':
        # Get all the properties
        properties1 = PropertyType1.objects.filter(is_listed=True)
        properties2 = PropertyType2.objects.filter(is_listed=True)
        properties3 = PropertyType3.objects.filter(is_listed=True)

        # Apply the filters to each queryset
        filters1 = PropertyType1Filter(request.GET, queryset=properties1)
        filters2 = PropertyType2Filter(request.GET, queryset=properties2)
        filters3 = PropertyType3Filter(request.GET, queryset=properties3)

        # Combine the filtered properties
        properties = list(chain(filters1.qs, filters2.qs, filters3.qs))

        # Ordering
        ordering_value = request.query_params.get('ordering', None)
        if ordering_value:
            if ordering_value.startswith('-'):
                ordering_value = ordering_value[1:]
                ordering_direction = '-'
            else:
                ordering_direction = ''

            if ordering_value in ['expected_price', 'created_time', 'price_per_sq_ft']:
                properties.sort(key=lambda p: getattr(p, ordering_value), reverse=ordering_direction=='-')

        # Pagination
        paginator = SmallResultsSetPagination()
        paginated_properties = paginator.paginate_queryset(properties, request)

        # Serialization
        serializer_data = []
        for property in paginated_properties:
            if isinstance(property, PropertyType1):
                serializer = PropertyType1Serializer(property)
            elif isinstance(property, PropertyType2):
                serializer = PropertyType2Serializer(property)
            elif isinstance(property, PropertyType3):
                serializer = PropertyType3Serializer(property)
            serializer_data.append(serializer.data)

        return Response(serializer_data)

@api_view(['GET'])
def get_all_smallcard_properties(request):
    if request.method == 'GET':
        properties1 = PropertyType1.objects.filter(is_listed=True)
        properties2 = PropertyType2.objects.filter(is_listed=True)
        properties3 = PropertyType3.objects.filter(is_listed=True)

        filters1 = PropertyType1Filter(request.GET, queryset=properties1)
        filters2 = PropertyType2Filter(request.GET, queryset=properties2)
        filters3 = PropertyType3Filter(request.GET, queryset=properties3)

        properties = list(chain(filters1.qs, filters2.qs, filters3.qs))

        ordering_value = request.query_params.get('ordering', None)
        if ordering_value:
            if ordering_value.startswith('-'):
                ordering_value = ordering_value[1:]
                ordering_direction = '-'
            else:
                ordering_direction = ''

            if ordering_value in ['expected_price', 'created_time', 'price_per_sq_ft']:
                properties.sort(key=lambda p: getattr(p, ordering_value), reverse=ordering_direction=='-')

        paginator = SmallResultsSetPagination()
        paginated_properties = paginator.paginate_queryset(properties, request)

        # Serialization
        serializer_data = []
        for property in paginated_properties:
            if isinstance(property, PropertyType1):
                serializer = PropertyType1SmallCardSerializer(property)
            elif isinstance(property, PropertyType2):
                serializer = PropertyType2SmallCardSerializer(property)
            elif isinstance(property, PropertyType3):
                serializer = PropertyType3SmallCardSerializer(property)
            serializer_data.append(serializer.data)

        return Response(serializer_data)
    
@api_view(['GET'])
def get_all_largecard_properties(request):
    if request.method == 'GET':
        properties1 = PropertyType1.objects.filter(is_listed=True)
        properties2 = PropertyType2.objects.filter(is_listed=True)
        properties3 = PropertyType3.objects.filter(is_listed=True)

        filters1 = PropertyType1Filter(request.GET, queryset=properties1)
        filters2 = PropertyType2Filter(request.GET, queryset=properties2)
        filters3 = PropertyType3Filter(request.GET, queryset=properties3)

        properties = list(chain(filters1.qs, filters2.qs, filters3.qs))

        ordering_value = request.query_params.get('ordering', None)
        if ordering_value:
            if ordering_value.startswith('-'):
                ordering_value = ordering_value[1:]
                ordering_direction = '-'
            else:
                ordering_direction = ''

            if ordering_value in ['expected_price', 'created_time', 'price_per_sq_ft']:
                properties.sort(key=lambda p: getattr(p, ordering_value), reverse=ordering_direction=='-')

        paginator = SmallResultsSetPagination()
        paginated_properties = paginator.paginate_queryset(properties, request)

        # Serialization
        serializer_data = []
        for property in paginated_properties:
            if isinstance(property, PropertyType1):
                serializer = PropertyType1LargeCardSerializer(property)
            elif isinstance(property, PropertyType2):
                serializer = PropertyType2LargeCardSerializer(property)
            elif isinstance(property, PropertyType3):
                serializer = PropertyType3LargeCardSerializer(property)
            serializer_data.append(serializer.data)

        return Response(serializer_data)

@api_view(['GET'])
def crm_card_combined(request):
    status_filter = request.GET.get('status', None)
    
    if not status_filter:
        return Response({"detail": "No Status Detected."}, status=status.HTTP_400_BAD_REQUEST)

    crm_cards_combined = []
    
    # PropertyType1
    if status_filter in dict(PropertyType1.CRM_STATUS_CHOICES).keys():
        crm_cards1 = PropertyType1.objects.filter(status=status_filter)
        filters1 = PropertyType1Filter(request.GET, queryset=crm_cards1)
        serializer1 = PropertyType1CRMSerializer(filters1.qs, many=True)
        crm_cards_combined.extend(serializer1.data)
        
    # PropertyType2
    if status_filter in dict(PropertyType2.CRM_STATUS_CHOICES).keys():
        crm_cards2 = PropertyType2.objects.filter(status=status_filter)
        filters2 = PropertyType2Filter(request.GET, queryset=crm_cards2)
        serializer2 = PropertyType2CRMSerializer(filters2.qs, many=True)
        crm_cards_combined.extend(serializer2.data)
    
    # PropertyType3
    if status_filter in dict(PropertyType3.CRM_STATUS_CHOICES).keys():
        crm_cards3 = PropertyType3.objects.filter(status=status_filter)
        filters3 = PropertyType3Filter(request.GET, queryset=crm_cards3)
        serializer3 = PropertyType3CRMSerializer(filters3.qs, many=True)
        crm_cards_combined.extend(serializer3.data)

    if not crm_cards_combined:
        return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(crm_cards_combined)

class count(APIView):
    def post(self, request):
        call_type = request.data.get('call_type')
        broker_id = request.data.get('id')

        if not call_type or not broker_id:
            return Response({'error': 'Call type and ID are required.'}, status=400)

        counter, created = Counter.objects.get_or_create(id=broker_id)
        
        if call_type == 'meet':
            counter.meet_calls += 1
        elif call_type == 'chat':
            counter.chat_calls += 1
        elif call_type == 'property':
            counter.property_calls += 1
        else:
            return Response({'error': 'Invalid call type.'}, status=400)

        counter.save()

        return Response({'success': 'Call count updated successfully.'})


class countview(APIView):
    def post(self, request):
        call_type = request.data.get('call_type')
        id = request.data.get('id')

        if not call_type or not id:
            return Response({'error': 'Call type and ID are required.'}, status=400)

        counter = Counter.objects.filter(id=id).first()

        if not counter:
            return Response({'error': 'Counter not found.'}, status=404)

        hit_count = 0

        if call_type == 'meet':
            hit_count = counter.meet_calls
        elif call_type == 'chat':
            hit_count = counter.chat_calls
        elif call_type == 'property':
            hit_count = counter.property_calls
        else:
            return Response({'error': 'Invalid call type.'}, status=400)

        return Response({'hits': hit_count})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import TokenError, AccessToken

@api_view(['POST'])
def location_page(request):
    # Retrieve the token from the Authorization header
    authorization_header = request.headers.get('Authorization', '')
    token = authorization_header.split('Bearer ')[-1].strip()

    # Verify the token
    try:
        AccessToken(token)
        gmaps = googlemaps.Client(key='AIzaSyCzkfZU5H2EfmRZdzubLoVas9t8E32uroU')
        location = gmaps.geolocate()
        latlng = location['location']
        geocode_result = gmaps.reverse_geocode((latlng['lat'], latlng['lng']))
        city = ""
    
        for component in geocode_result[0]['address_components']:
            if 'locality' or 'sublocality'  in component['types']:
                city = city +" "+ component['long_name']
                
        return JsonResponse({'city': city})
    except TokenError as e:
        # Token is invalid, return an error response
        return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import TokenError, AccessToken

@api_view(['POST'])
def get_user_location(request):
    # Retrieve the token from the Authorization header
    authorization_header = request.headers.get('Authorization', '')
    token = authorization_header.split('Bearer ')[-1].strip()

    # Verify the token
    try:
        AccessToken(token)
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        return JsonResponse({'message': 'Location received'})
        return Response({'detail': 'Access granted'}, status=status.HTTP_200_OK)
    except TokenError as e:
        # Token is invalid, return an error response
        return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


# class location_page(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
    
    
#     def get(self,request):
#         gmaps = googlemaps.Client(key='AIzaSyCzkfZU5H2EfmRZdzubLoVas9t8E32uroU')
#         location = gmaps.geolocate()
#         latlng = location['location']
#         geocode_result = gmaps.reverse_geocode((latlng['lat'], latlng['lng']))
#         city = ""
    
#         for component in geocode_result[0]['address_components']:
#             if 'locality' or 'sublocality'  in component['types']:
#                 city = city +" "+ component['long_name']
                
#         return JsonResponse({'city': city})
    
# def get_user_location(request):
#     latitude = request.GET.get('latitude')
#     longitude = request.GET.get('longitude')
#     # Process the latitude and longitude as needed
#     # ...
#     return JsonResponse({'message': 'Location received'})


#TYPE 1 VIEWS
@api_view(['POST'])
def create_type1(request):
    serializer = PropertyType1Serializer(data=request.data)
    
    if serializer.is_valid():
        main_image = request.FILES.get('main_image')
        additional_images = request.FILES.getlist('additional_images')
        s3 = boto3.client('s3', aws_access_key_id=os.environ['KEY_ID'], aws_secret_access_key=os.environ['ACCESS_KEY'])
        bucket = 'propscan.s00'
        additional_image_links = []

        # Upload main image
        if main_image:
            unique_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(main_image.name)[1]
            filename = f"uploads/property_images_type1/{unique_filename}{file_extension}"

            try:
                s3.upload_fileobj(Fileobj=main_image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                serializer.validated_data['main_image_link'] = file_url
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Upload additional images
        for image in additional_images:
            unique_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(image.name)[1]
            filename = f"uploads/property_images_type1/{unique_filename}{file_extension}"

            try:
                s3.upload_fileobj(Fileobj=image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                additional_image_links.append(file_url)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer.validated_data['additional_images_link'] = ','.join(additional_image_links)
        serializer.save()
        return Response({"message": "Property Created Successfully"}, status=status.HTTP_201_CREATED)
    
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def getfull_type1(request):
    # properties = PropertyType1.objects.filter(is_listed=True)
    # filters = PropertyType1Filter(request.GET, queryset=properties)
    # serializer = PropertyType1Serializer(filters.qs, many=True)
    # return Response(serializer.data)
# AIzaSyCzkfZU5H2EfmRZdzubLoVas9t8E32uroU
@api_view(['GET', 'POST'])
def getfull_type1(request):
    if request.method == 'GET':
        properties = PropertyType1.objects.filter(is_listed=True)
        filters = PropertyType1Filter(request.GET, queryset=properties)
        
        ordering_value = request.query_params.get('ordering', None)
        if ordering_value:
            if ordering_value.startswith('-'):
                ordering_value = ordering_value[1:]
                ordering_direction = '-'
            else:
                ordering_direction = ''
            
            if ordering_value in ['expected_price', 'created_time', 'price_per_sq_ft']:  # add any other fields you want to allow ordering by here
                ordered_queryset = filters.qs.order_by(f"{ordering_direction}{ordering_value}")
            else:
                ordered_queryset = filters.qs
        else:
            ordered_queryset = filters.qs
        
        paginator = SmallResultsSetPagination()
        paginated_properties = paginator.paginate_queryset(ordered_queryset, request)
        serializer = PropertyType1Serializer(paginated_properties, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        location = request.data.get('location')
        distance = request.data.get('distance')

        properties = PropertyType1.objects.filter(is_listed=True)
        print(properties)
        serialized_properties = []
        for prop in properties:
            city = prop.city

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
                print(distance_value,city,location)
                if distance_value is not None and distance_value < distance:
                    prop_data = PropertyType1Serializer(prop).data
                    prop_data['distance'] = distance_value
                    serialized_properties.append(prop_data)
            else:
                prop_data = PropertyType1Serializer(prop).data
                prop_data['distance'] = None
                serialized_properties.append(prop_data)

        return Response(serialized_properties)

# @api_view(['GET'])
# def smallcard_type1(request):
#     properties = PropertyType1.objects.filter(is_listed=True)
#     filters = PropertyType1Filter(request.GET, queryset=properties)
#     serializer = PropertyType1SmallCardSerializer(filters.qs, many=True)
#     return Response(serializer.data)
@api_view(['GET', 'POST'])
def smallcard_type1(request):
    if request.method == 'GET':
        properties = PropertyType1.objects.filter(is_listed=True)
        filters = PropertyType1Filter(request.GET, queryset=properties)
        
        ordering_value = request.query_params.get('ordering', None)
        if ordering_value:
            if ordering_value.startswith('-'):
                ordering_value = ordering_value[1:]
                ordering_direction = '-'
            else:
                ordering_direction = ''
            
            if ordering_value in ['expected_price', 'created_time', 'price_per_sq_ft']:  # add any other fields you want to allow ordering by here
                ordered_queryset = filters.qs.order_by(f"{ordering_direction}{ordering_value}")
            else:
                ordered_queryset = filters.qs
        else:
            ordered_queryset = filters.qs
        
        paginator = SmallResultsSetPagination()
        paginated_properties = paginator.paginate_queryset(ordered_queryset, request)
        serializer = PropertyType1SmallCardSerializer(paginated_properties, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        location = request.data.get('location')
        distance = request.data.get('distance')

        properties = PropertyType1.objects.filter(is_listed=True)

        serialized_properties = []
        for prop in properties:
            city = prop.city

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
                    prop_data = PropertyType1SmallCardSerializer(prop).data
                    prop_data['distance'] = distance_value
                    serialized_properties.append(prop_data)
            else:
                prop_data = PropertyType1SmallCardSerializer(prop).data
                prop_data['distance'] = None
                serialized_properties.append(prop_data)

        return Response(serialized_properties)

# @api_view(['GET'])
# def largecard_type1(request):
#     properties = PropertyType1.objects.filter(is_listed=True)
#     filters = PropertyType1Filter(request.GET, queryset=properties)
#     serializer = PropertyType1LargeCardSerializer(filters.qs, many=True)
#     return Response(serializer.data)
@api_view(['GET', 'POST'])
def largecard_type1(request):
    if request.method == 'GET':
        properties = PropertyType1.objects.filter(is_listed=True)
        filters = PropertyType1Filter(request.GET, queryset=properties)
        serializer = PropertyType1LargeCardSerializer(filters.qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        location = request.data.get('location')
        distance = request.data.get('distance')

        properties = PropertyType1.objects.filter(is_listed=True)

        serialized_properties = []
        for prop in properties:
            city = prop.city

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
                    prop_data = PropertyType1LargeCardSerializer(prop).data
                    prop_data['distance'] = distance_value
                    serialized_properties.append(prop_data)
            else:
                prop_data = PropertyType1LargeCardSerializer(prop).data
                prop_data['distance'] = None
                serialized_properties.append(prop_data)

        return Response(serialized_properties)

@api_view(['PUT'])
def unlist_type1(request, property_id):
    try:
        property_instance = PropertyType1.objects.get(pk=property_id)
    except PropertyType1.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    property_instance.is_listed = False
    property_instance.status = 'Unlisted'
    property_instance.save()

    serializer = PropertyType1Serializer(property_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def sell_property_type1(request, property_id):
    try:
        property_instance = PropertyType1.objects.get(pk=property_id)
    except PropertyType1.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    property_instance.is_listed = False
    property_instance.status = 'Sold'
    property_instance.sold_date = date.today()

    final_selling_price = request.data.get('final_selling_price')
    if final_selling_price:
        property_instance.final_selling_price = final_selling_price

    property_instance.save()

    serializer = PropertyType1Serializer(property_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_property_type1(request, pk):
    property_instance = get_object_or_404(PropertyType1, pk=pk)
    serializer = PropertyType1Serializer(instance=property_instance, data=request.data, partial=True)

    if serializer.is_valid():
        main_image = request.FILES.get('main_image')
        additional_images = request.FILES.getlist('additional_images')
        s3 = boto3.client('s3', aws_access_key_id=os.environ['KEY_ID'], aws_secret_access_key=os.environ['ACCESS_KEY'])
        bucket = 'propscan.s00'
        additional_image_links = []

        # Update main image
        if main_image:
            unique_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(main_image.name)[1]
            filename = f"uploads/property_images_type1/{unique_filename}{file_extension}"

            try:
                s3.upload_fileobj(Fileobj=main_image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                serializer.validated_data['main_image_link'] = file_url
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Update additional images
        if additional_images:
            for image in additional_images:
                unique_filename = str(uuid.uuid4())
                file_extension = os.path.splitext(image.name)[1]
                filename = f"uploads/property_images_type1/{unique_filename}{file_extension}"

                try:
                    s3.upload_fileobj(Fileobj=image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                    file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                    additional_image_links.append(file_url)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            serializer.validated_data['additional_images_link'] = ','.join(additional_image_links)

        serializer.save()
        return Response({"message": "Property Updated Successfully"}, status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#TYPE2 VIEWS
@api_view(['POST'])
def create_type2(request):
    serializer = PropertyType2Serializer(data=request.data)
    
    if serializer.is_valid():
        main_image = request.FILES.get('main_image')
        additional_images = request.FILES.getlist('additional_images')
        s3 = boto3.client('s3', aws_access_key_id=os.environ['KEY_ID'], aws_secret_access_key=os.environ['ACCESS_KEY'])
        bucket = 'propscan.s00'
        additional_image_links = []

        # Upload main image
        if main_image:
            unique_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(main_image.name)[1]
            filename = f"uploads/property_images_type2/{unique_filename}{file_extension}"

            try:
                s3.upload_fileobj(Fileobj=main_image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                serializer.validated_data['main_image_link'] = file_url
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Upload additional images
        for image in additional_images:
            unique_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(image.name)[1]
            filename = f"uploads/property_images_type2/{unique_filename}{file_extension}"

            try:
                s3.upload_fileobj(Fileobj=image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                additional_image_links.append(file_url)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer.validated_data['additional_images_link'] = ','.join(additional_image_links)
        serializer.save()
        return Response({"message": "Property Created Successfully"}, status=status.HTTP_201_CREATED)
    
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET'])
# def getfull_type2(request):
#     properties = PropertyType2.objects.filter(is_listed=True)
#     filters = PropertyType2Filter(request.GET, queryset=properties)
#     serializer = PropertyType2Serializer(filters.qs, many=True)
#     return Response(serializer.data)
@api_view(['GET', 'POST'])
def getfull_type2(request):
    if request.method == 'GET':
        properties = PropertyType2.objects.filter(is_listed=True)
        filters = PropertyType2Filter(request.GET, queryset=properties)
        
        ordering_value = request.query_params.get('ordering', None)
        if ordering_value:
            if ordering_value.startswith('-'):
                ordering_value = ordering_value[1:]
                ordering_direction = '-'
            else:
                ordering_direction = ''
            
            if ordering_value in ['expected_price', 'created_time', 'price_per_sq_ft']:  # add any other fields you want to allow ordering by here
                ordered_queryset = filters.qs.order_by(f"{ordering_direction}{ordering_value}")
            else:
                ordered_queryset = filters.qs
        else:
            ordered_queryset = filters.qs
        
        paginator = SmallResultsSetPagination()
        paginated_properties = paginator.paginate_queryset(ordered_queryset, request)
        serializer = PropertyType2Serializer(paginated_properties, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        location = request.data.get('location')
        distance = request.data.get('distance')

        properties = PropertyType2.objects.filter(is_listed=True)

        serialized_properties = []
        for prop in properties:
            city = prop.city

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
                    prop_data = PropertyType2Serializer(prop).data
                    prop_data['distance'] = distance_value
                    serialized_properties.append(prop_data)
            else:
                prop_data = PropertyType2Serializer(prop).data
                prop_data['distance'] = None
                serialized_properties.append(prop_data)

        return Response(serialized_properties)

# @api_view(['GET'])
# def smallcard_type2(request):
#     properties = PropertyType2.objects.filter(is_listed=True)
#     filters = PropertyType2Filter(request.GET, queryset=properties)
#     serializer = PropertyType2SmallCardSerializer(filters.qs, many=True)
#     return Response(serializer.data)
@api_view(['GET', 'POST'])
def smallcard_type2(request):
    if request.method == 'GET':
        properties = PropertyType2.objects.filter(is_listed=True)
        filters = PropertyType2Filter(request.GET, queryset=properties)
        
        ordering_value = request.query_params.get('ordering', None)
        if ordering_value:
            if ordering_value.startswith('-'):
                ordering_value = ordering_value[1:]
                ordering_direction = '-'
            else:
                ordering_direction = ''
            
            if ordering_value in ['expected_price', 'created_time', 'price_per_sq_ft']:  # add any other fields you want to allow ordering by here
                ordered_queryset = filters.qs.order_by(f"{ordering_direction}{ordering_value}")
            else:
                ordered_queryset = filters.qs
        else:
            ordered_queryset = filters.qs
        
        paginator = SmallResultsSetPagination()
        paginated_properties = paginator.paginate_queryset(ordered_queryset, request)
        serializer = PropertyType2SmallCardSerializer(paginated_properties, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        location = request.data.get('location')
        distance = request.data.get('distance')

        properties = PropertyType2.objects.filter(is_listed=True)

        serialized_properties = []
        for prop in properties:
            city = prop.city

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
                    prop_data = PropertyType2SmallCardSerializer(prop).data
                    prop_data['distance'] = distance_value
                    serialized_properties.append(prop_data)
            else:
                prop_data = PropertyType2SmallCardSerializer(prop).data
                prop_data['distance'] = None
                serialized_properties.append(prop_data)

        return Response(serialized_properties)


# @api_view(['GET'])
# def largecard_type2(request):
#     properties = PropertyType2.objects.filter(is_listed=True)
#     filters = PropertyType2Filter(request.GET, queryset=properties)
#     serializer = PropertyType2LargeCardSerializer(filters.qs, many=True)
#     return Response(serializer.data)
@api_view(['GET', 'POST'])
def largecard_type2(request):
    if request.method == 'GET':
        properties = PropertyType2.objects.filter(is_listed=True)
        filters = PropertyType2Filter(request.GET, queryset=properties)
        serializer = PropertyType2LargeCardSerializer(filters.qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        location = request.data.get('location')
        distance = request.data.get('distance')

        properties = PropertyType2.objects.filter(is_listed=True)

        serialized_properties = []
        for prop in properties:
            city = prop.city

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
                    prop_data = PropertyType2LargeCardSerializer(prop).data
                    prop_data['distance'] = distance_value
                    serialized_properties.append(prop_data)
            else:
                prop_data = PropertyType2LargeCardSerializer(prop).data
                prop_data['distance'] = None
                serialized_properties.append(prop_data)

        return Response(serialized_properties)


@api_view(['PUT'])
def unlist_type2(request, property_id):
    try:
        property_instance = PropertyType2.objects.get(pk=property_id)
    except PropertyType2.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    property_instance.is_listed = False
    property_instance.status = 'Unlisted'
    property_instance.save()

    serializer = PropertyType2Serializer(property_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def sell_property_type2(request, property_id):
    try:
        property_instance = PropertyType2.objects.get(pk=property_id)
    except PropertyType2.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    property_instance.is_listed = False
    property_instance.status = 'Sold'
    property_instance.sold_date = date.today()

    final_selling_price = request.data.get('final_selling_price')
    if final_selling_price:
        property_instance.final_selling_price = final_selling_price

    property_instance.save()

    serializer = PropertyType2Serializer(property_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_property_type2(request, pk):
    property_instance = get_object_or_404(PropertyType2, pk=pk)
    serializer = PropertyType2Serializer(instance=property_instance, data=request.data, partial=True)

    if serializer.is_valid():
        main_image = request.FILES.get('main_image')
        additional_images = request.FILES.getlist('additional_images')
        s3 = boto3.client('s3', aws_access_key_id=os.environ['KEY_ID'], aws_secret_access_key=os.environ['ACCESS_KEY'])
        bucket = 'propscan.s00'
        additional_image_links = []

        # Update main image
        if main_image:
            unique_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(main_image.name)[1]
            filename = f"uploads/property_images_type2/{unique_filename}{file_extension}"

            try:
                s3.upload_fileobj(Fileobj=main_image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                serializer.validated_data['main_image_link'] = file_url
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Update additional images
        if additional_images:
            for image in additional_images:
                unique_filename = str(uuid.uuid4())
                file_extension = os.path.splitext(image.name)[1]
                filename = f"uploads/property_images_type2/{unique_filename}{file_extension}"

                try:
                    s3.upload_fileobj(Fileobj=image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                    file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                    additional_image_links.append(file_url)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            serializer.validated_data['additional_images_link'] = ','.join(additional_image_links)

        serializer.save()
        return Response({"message": "Property Updated Successfully"}, status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#TYPE3 VIEWS
@api_view(['POST'])
def create_type3(request):
    serializer = PropertyType3Serializer(data=request.data)
    
    if serializer.is_valid():
        main_image = request.FILES.get('main_image')
        additional_images = request.FILES.getlist('additional_images')
        s3 = boto3.client('s3', aws_access_key_id=os.environ['KEY_ID'], aws_secret_access_key=os.environ['ACCESS_KEY'])
        bucket = 'propscan.s00'
        additional_image_links = []

        # Upload main image
        if main_image:
            unique_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(main_image.name)[1]
            filename = f"uploads/property_images_type3/{unique_filename}{file_extension}"

            try:
                s3.upload_fileobj(Fileobj=main_image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                serializer.validated_data['main_image_link'] = file_url
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Upload additional images
        for image in additional_images:
            unique_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(image.name)[1]
            filename = f"uploads/property_images_type1/{unique_filename}{file_extension}"

            try:
                s3.upload_fileobj(Fileobj=image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                additional_image_links.append(file_url)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer.validated_data['additional_images_link'] = ','.join(additional_image_links)
        serializer.save()
        return Response({"message": "Property Created Successfully"}, status=status.HTTP_201_CREATED)
    
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def getfull_type3(request):
#     properties = PropertyType3.objects.filter(is_listed=True)
#     filters = PropertyType3Filter(request.GET, queryset=properties)
#     serializer = PropertyType3Serializer(filters.qs, many=True)
#     return Response(serializer.data)
@api_view(['GET', 'POST'])
def getfull_type3(request):
    if request.method == 'GET':
        properties = PropertyType3.objects.filter(is_listed=True)
        filters = PropertyType3Filter(request.GET, queryset=properties)
        
        ordering_value = request.query_params.get('ordering', None)
        if ordering_value:
            if ordering_value.startswith('-'):
                ordering_value = ordering_value[1:]
                ordering_direction = '-'
            else:
                ordering_direction = ''
            
            if ordering_value in ['expected_price', 'created_time', 'price_per_sq_ft']:  # add any other fields you want to allow ordering by here
                ordered_queryset = filters.qs.order_by(f"{ordering_direction}{ordering_value}")
            else:
                ordered_queryset = filters.qs
        else:
            ordered_queryset = filters.qs
        
        paginator = SmallResultsSetPagination()
        paginated_properties = paginator.paginate_queryset(ordered_queryset, request)
        serializer = PropertyType3Serializer(paginated_properties, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        location = request.data.get('location')
        distance = request.data.get('distance')

        properties = PropertyType3.objects.filter(is_listed=True)

        serialized_properties = []
        for prop in properties:
            city = prop.city

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
                    prop_data = PropertyType3Serializer(prop).data
                    prop_data['distance'] = distance_value
                    serialized_properties.append(prop_data)
            else:
                prop_data = PropertyType3Serializer(prop).data
                prop_data['distance'] = None
                serialized_properties.append(prop_data)

        return Response(serialized_properties)
    
# @api_view(['GET'])
# def smallcard_type3(request):
#     properties = PropertyType3.objects.filter(is_listed=True)
#     filters = PropertyType3Filter(request.GET, queryset=properties)
#     serializer = PropertyType3SmallCardSerializer(filters.qs, many=True)
#     return Response(serializer.data)
@api_view(['GET', 'POST'])
def smallcard_type3(request):
    if request.method == 'GET':
        properties = PropertyType3.objects.filter(is_listed=True)
        filters = PropertyType3Filter(request.GET, queryset=properties)
        
        ordering_value = request.query_params.get('ordering', None)
        if ordering_value:
            if ordering_value.startswith('-'):
                ordering_value = ordering_value[1:]
                ordering_direction = '-'
            else:
                ordering_direction = ''
            
            if ordering_value in ['expected_price', 'created_time', 'price_per_sq_ft']:  # add any other fields you want to allow ordering by here
                ordered_queryset = filters.qs.order_by(f"{ordering_direction}{ordering_value}")
            else:
                ordered_queryset = filters.qs
        else:
            ordered_queryset = filters.qs
        
        paginator = SmallResultsSetPagination()
        paginated_properties = paginator.paginate_queryset(ordered_queryset, request)
        serializer = PropertyType3SmallCardSerializer(paginated_properties, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        location = request.data.get('location')
        distance = request.data.get('distance')

        properties = PropertyType3.objects.filter(is_listed=True)

        serialized_properties = []
        for prop in properties:
            city = prop.city

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
                    prop_data = PropertyType3SmallCardSerializer(prop).data
                    prop_data['distance'] = distance_value
                    serialized_properties.append(prop_data)
            else:
                prop_data = PropertyType3SmallCardSerializer(prop).data
                prop_data['distance'] = None
                serialized_properties.append(prop_data)

        return Response(serialized_properties)
    
    
# @api_view(['GET'])
# def largecard_type3(request):
#     properties = PropertyType3.objects.filter(is_listed=True)
#     filters = PropertyType3Filter(request.GET, queryset=properties)
#     serializer = PropertyType3LargeCardSerializer(filters.qs, many=True)
#     return Response(serializer.data)
@api_view(['GET', 'POST'])
def largecard_type3(request):
    if request.method == 'GET':
        properties = PropertyType3.objects.filter(is_listed=True)
        filters = PropertyType3Filter(request.GET, queryset=properties)
        serializer = PropertyType3LargeCardSerializer(filters.qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        location = request.data.get('location')
        distance = request.data.get('distance')

        properties = PropertyType3.objects.filter(is_listed=True)

        serialized_properties = []
        for prop in properties:
            city = prop.city

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
                    prop_data = PropertyType3LargeCardSerializer(prop).data
                    prop_data['distance'] = distance_value
                    serialized_properties.append(prop_data)
            else:
                prop_data = PropertyType3LargeCardSerializer(prop).data
                prop_data['distance'] = None
                serialized_properties.append(prop_data)

        return Response(serialized_properties)

@api_view(['PUT'])
def unlist_type3(request, property_id):
    try:
        property_instance = PropertyType3.objects.get(pk=property_id)
    except PropertyType3.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    property_instance.is_listed = False
    property_instance.status = 'Unlisted'
    property_instance.save()

    serializer = PropertyType3Serializer(property_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def sell_property_type3(request, property_id):
    try:
        property_instance = PropertyType3.objects.get(pk=property_id)
    except PropertyType3.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    property_instance.is_listed = False
    property_instance.status = 'Sold'
    property_instance.sold_date = date.today()

    final_selling_price = request.data.get('final_selling_price')
    if final_selling_price:
        property_instance.final_selling_price = final_selling_price

    property_instance.save()

    serializer = PropertyType3Serializer(property_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_property_type3(request, pk):
    property_instance = get_object_or_404(PropertyType3, pk=pk)
    serializer = PropertyType3Serializer(instance=property_instance, data=request.data, partial=True)

    if serializer.is_valid():
        main_image = request.FILES.get('main_image')
        additional_images = request.FILES.getlist('additional_images')
        s3 = boto3.client('s3', aws_access_key_id=os.environ['KEY_ID'], aws_secret_access_key=os.environ['ACCESS_KEY'])
        bucket = 'propscan.s00'
        additional_image_links = []

        # Update main image
        if main_image:
            unique_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(main_image.name)[1]
            filename = f"uploads/property_images_type3/{unique_filename}{file_extension}"

            try:
                s3.upload_fileobj(Fileobj=main_image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                serializer.validated_data['main_image_link'] = file_url
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Update additional images
        if additional_images:
            for image in additional_images:
                unique_filename = str(uuid.uuid4())
                file_extension = os.path.splitext(image.name)[1]
                filename = f"uploads/property_images_type3/{unique_filename}{file_extension}"

                try:
                    s3.upload_fileobj(Fileobj=image, Bucket=bucket, Key=filename, ExtraArgs={'ACL': 'public-read'})
                    file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
                    additional_image_links.append(file_url)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            serializer.validated_data['additional_images_link'] = ','.join(additional_image_links)

        serializer.save()
        return Response({"message": "Property Updated Successfully"}, status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#CRM VIEWS

#TYPE 1
@api_view(['PUT'])
def update_crm_status_type1(request, id):
    try:
        property_instance = PropertyType1.objects.get(pk=id)
    except PropertyType1.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    status_data = request.data.get('status')
    if status_data in dict(PropertyType1.CRM_STATUS_CHOICES).keys():  # Making sure the status is valid
        property_instance.status = status_data
        property_instance.save()
    else:
        return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = PropertyType1Serializer(property_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)



#TYPE 2

@api_view(['PUT'])
def update_crm_status_type2(request, id):
    try:
        property_instance = PropertyType2.objects.get(pk=id)
    except PropertyType2.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    status_data = request.data.get('status')
    if status_data in dict(PropertyType2.CRM_STATUS_CHOICES).keys():  # Making sure the status is valid
        property_instance.status = status_data
        property_instance.save()
    else:
        return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = PropertyType2Serializer(property_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)



#TYPE 3

@api_view(['PUT'])
def update_crm_status_type3(request, id):
    try:
        property_instance = PropertyType3.objects.get(pk=id)
    except PropertyType3.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    status_data = request.data.get('status')
    if status_data in dict(PropertyType3.CRM_STATUS_CHOICES).keys():  # Make sure the status is valid
        property_instance.status = status_data
        property_instance.save()
    else:
        return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = PropertyType3Serializer(property_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)


#crm card views

@api_view(['GET'])
def crm_card_type1(request):
    status_filter = request.GET.get('status', None)
    if status_filter:
        if status_filter not in dict(PropertyType1.CRM_STATUS_CHOICES).keys():  # Make sure the status is valid
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        crm_cards = PropertyType1.objects.filter(status=status_filter)
    else:
        return Response({"detail": "No Status Detected."}, status=status.HTTP_400_BAD_REQUEST)
    
    filters = PropertyType1Filter(request.GET, queryset=crm_cards)
    serializer = PropertyType1CRMSerializer(filters.qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def crm_card_type2(request):
    status_filter = request.GET.get('status', None)

    if status_filter:
        if status_filter not in dict(PropertyType2.CRM_STATUS_CHOICES).keys():  # Make sure the status is valid
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        crm_cards = PropertyType2.objects.filter(status=status_filter)
    else:
        return Response({"detail": "No Status Detected"}, status=status.HTTP_400_BAD_REQUEST)

    filters = PropertyType2Filter(request.GET, queryset=crm_cards)
    serializer = PropertyType2CRMSerializer(filters.qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def crm_card_type3(request):
    status_filter = request.GET.get('status', None)

    if status_filter:
        if status_filter not in dict(PropertyType3.CRM_STATUS_CHOICES).keys():  # Make sure the status is valid
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        crm_cards = PropertyType3.objects.filter(status=status_filter)
    else:
        return Response({"detail": "No Status Detected"}, status=status.HTTP_400_BAD_REQUEST)
    
    filters = PropertyType3Filter(request.GET, queryset=crm_cards)
    serializer = PropertyType3CRMSerializer(filters.qs, many=True)
    return Response(serializer.data)


#CRM CONTACTED API
@api_view(['PUT'])
def update_contacted_status_type1(request,id):
    try:
        property_instance = PropertyType1.objects.get(pk=id)
    except PropertyType1.DoesNotExist:
        return Response({"detal": "Property not found"}, status=status.HTTP_404_NOT_FOUND)
    
    property_instance.contacted=True
    property_instance.save()
    serializer = PropertyType1Serializer(property_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_contacted_status_type2(request,id):
    try:
        property_instance = PropertyType2.objects.get(pk=id)
    except PropertyType2.DoesNotExist: 
        return Response({"detail": "Property not found"}, status=status.HTTP_404_NOT_FOUND)
        
    property_instance.contacted=True
    property_instance.save()
    serializer = PropertyType2Serializer(property_instance)
    return Response(serializer.date, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_contacted_status_type3(request, id):
    try:
        property_instance = PropertyType3.objects.get(pk=id)
    except PropertyType3.DoesNotExist:
        return Response({"detail": "Property not found"},status=status.HTTP_404_NOT_FOUND)
    
    property_instance.contacted=True
    property_instance.save()
    serializer = PropertyType3Serializer(property_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)
