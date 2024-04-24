from django.shortcuts import render, redirect
from .models import ChatRoom, Message
import json

from django.http import JsonResponse

def room(request, room_name):
    chatroom, created = ChatRoom.objects.get_or_create(name=room_name)
    
    # Search messages based on query parameter (if provided)
    search_query = request.GET.get('q', '')  # Get the search query from the request URL
    if search_query:
        chat_messages = Message.objects.filter(chatroom=chatroom, message__icontains=search_query)
    else:
        chat_messages = Message.objects.filter(chatroom=chatroom)

    # Serialize chat messages to a list of dictionaries
    serialized_messages = [
        {
            'id': message.id,
            'user': message.user.username,
            'message': message.message,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in chat_messages
    ]

    context = {
        'room_name': room_name,
        'chat_messages': serialized_messages,
        'current_user': request.user.username
    }

    return JsonResponse(context)
from django.views import View


class DeleteConversationView(View):
    def post(self, request, room_name):
        try:
            chatroom = ChatRoom.objects.get(name=room_name)

            # Delete all chat messages in the chat room
            Message.objects.filter(chatroom=chatroom).delete()

            return JsonResponse({'message': 'Conversation deleted successfully'})

        except ChatRoom.DoesNotExist:
            return JsonResponse({'error': 'Chat room not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class BlockUserView(View):
    def post(self, request, room_name):
        try:
            chatroom = ChatRoom.objects.get(name=room_name)
            blocked_username = request.POST.get('blocked_username')
            user_to_block = User.objects.get(username=blocked_username)

            # Check if the user is already blocked
            if BlockedUser.objects.filter(chatroom=chatroom, blocked_user=user_to_block).exists():
                return JsonResponse({'error': 'User is already blocked'}, status=400)

            # Block the user
            BlockedUser.objects.create(chatroom=chatroom, blocked_user=user_to_block)

            return JsonResponse({'message': f'User {blocked_username} has been blocked successfully'})

        except ChatRoom.DoesNotExist:
            return JsonResponse({'error': 'Chat room not found'}, status=404)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)