from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token


from .serializers import MessagesSerializer
from django.http import HttpResponse
from django.template import loader



from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
@api_view(['GET'])
def ApiOverview(request):
	api_urls = {

        'add-users': 'create/' ,
        'update-items': 'update/',
        'delete_message': 'deletemessage/',
        'send-message': 'sendmessage/',
        'viewsentmessages': 'viewsentmessages/',
        'viewreceivedmessages': 'viewreceivedmessages/'
	}

	return Response(api_urls)


from rest_framework import status



#send message
@login_required
@api_view(['POST'])
def send_message(request):
	username = request.user.username
	request.data._mutable = True
	request.data["sender"] = username
	request.data._mutable = False
	print(request.data)
	message = MessagesSerializer(data=request.data)

	# validating for recipient
	if not User.objects.filter(username = request.data["receiver"]).exists():
		return Response( data="This recipient does not exist." ,status=status.HTTP_404_NOT_FOUND)
	
	else:


		if message.is_valid():
			message.save()
			return Response(message.data)
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)


#view sent messages
@login_required
@api_view(['GET'])
def view_sent_messages(request):

	username = request.user
	print(username)
	
	# sender = request.data[""]
	# checking for the parameters from the URL
	username = request.user
	items =  Messages.objects.filter(sender = username, sender_delete_status = False).all().values()


	# if there is something in items else raise error
	if items:
		serializer = MessagesSerializer(items, many=True)
		return Response(serializer.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)

#view received messages
@login_required
@api_view(['GET'])
def view_received_messages(request):
	
	
	# checking for the parameters from the URL
	username = request.user
	items =  Messages.objects.filter(receiver = username, receiver_delete_status = False).all().values()


	# if there is something in items else raise error
	if items:
		serializer = MessagesSerializer(items, many=True)
		return Response(serializer.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)




#delete message
@login_required
@api_view(['POST'])
def delete_message(request):
	print(request.data)
	username = request.user.username
	record_id = request.data["id"]

	obj = Messages.objects.get(pk=record_id)
	if obj:

		if username == obj.sender:
			obj.sender_delete_status = True
		if username == obj.receiver:
			obj.receiver_delete_status = True
		obj.save()

		return Response(status=status.HTTP_202_ACCEPTED)
	else:
	 	return Response(status=status.HTTP_404_NOT_FOUND)

@login_required
def inbox(request):
	username = request.user
	messages =  Messages.objects.filter(receiver = username, receiver_delete_status = False).all().values()


	# if there is something in items else raise error
	if messages:
		serializer = MessagesSerializer(messages, many=True)
		

		context = {
    	'messages': serializer.data,
  			}
		template = loader.get_template('inbox.html')
	
		return HttpResponse(template.render(context, request))
	else:
		template = loader.get_template('inbox.html')
		context = {
    	'user': request.user }
		return HttpResponse(template.render(context,request))

   

@login_required
def sentbox(request):
	username = request.user
	print(username)
	messages =  Messages.objects.filter(sender = username, sender_delete_status = False).all().values()
	# print(mymembers)
	if messages:
		serializer = MessagesSerializer(messages, many=True)
		
		print(serializer.data)
		context = {
    	'messages': serializer.data }
		template = loader.get_template('sentbox.html')
	
		return HttpResponse(template.render(context, request))
	else:
		template = loader.get_template('sentbox.html')
		context = {
    	'user': request.user }
		return HttpResponse(template.render(context,request))


@requires_csrf_token
def compose(request):
	c = {}
	template = loader.get_template('compose.html')
	context = {
    	'user': request.user }
	return HttpResponse(template.render(context, request))
