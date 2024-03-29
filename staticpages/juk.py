
# from .models import Message, Reaction, UserProfile
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
# from django.utils import timezone

# @login_required
# def chat_room(request):
#     messages = Message.objects.all()
#     for message in messages:
#         message.read = True
#         message.save()
#     return render(request, 'marketplace/chat_room.html', {'messages': messages})

# @login_required
# def send_message(request):
#     if request.method == 'POST':
#         user = request.user
#         message_content = request.POST.get('message', '')

#         if message_content.strip():
#             # Save message to database
#             message = Message.objects.create(user=user, content=message_content)

#             # Send message to the channel layer with timestamp
#             timestamp = message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.group_send)(
#                 'chat_room',
#                 {
#                     'type': 'chat_message',
#                     'username': user.username,
#                     'message': message_content,
#                     'timestamp': timestamp
#                 }
#             )

#             return JsonResponse({'status': 'success'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'})

# @login_required
# def clear_messages(request):
#     Message.objects.all().delete()
#     return JsonResponse({'status': 'success'})

# @login_required
# def get_messages(request):
#     messages = Message.objects.all()
#     data = [{'username': message.user.username, 'message': message.content, 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for message in messages]
#     return JsonResponse(data, safe=False)

# @login_required
# @csrf_exempt
# def typing_status(request):
#     if request.method == 'POST':
#         user = request.user
#         typing = request.POST.get('typing', 'false')

#         # Broadcast typing status to other users in the chat room
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'chat_room',
#             {
#                 'type': 'typing_status',
#                 'username': user.username,
#                 'typing': typing
#             }
#         )
#         return HttpResponse('OK')

# @login_required
# def add_reaction(request):
#     if request.method == 'POST':
#         user = request.user
#         message_id = request.POST.get('message_id')
#         emoji = request.POST.get('emoji')

#         message = Message.objects.get(id=message_id)
#         reaction, created = Reaction.objects.get_or_create(emoji=emoji, user=user)

#         message.reactions.add(reaction)

#         return JsonResponse({'status': 'success'})

