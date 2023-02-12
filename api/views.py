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
from rest_framework import status




class SignUpView(generic.CreateView):
	""" Returns a signup template

    Args:
    generic.CreateView: A view that displays a form for creating an object.

    Returns:
      None

    """
	form_class = UserCreationForm
	success_url = reverse_lazy("login")
	template_name = "registration/signup.html"

#list of allowed methods
@login_required
@api_view(['GET'])
def ApiOverview(request):

	""" Returns a resposnse of allowed methods

    Args:
    request

    Returns:
    Dictionary of allowed methods

    Raises:
    None """

	api_urls = {

        'delete_message': 'deletemessage/',
        'send-message': 'sendmessage/',
        'viewsentmessages': 'viewsentmessages/',
        'viewreceivedmessages': 'viewreceivedmessages/'
	}

	return Response(api_urls)



#send message
@login_required
@api_view(['POST'])
def send_message(request):

	""" Sends a message from current logged in user to recipient

    Args:
    POST request data containing message body, title and recipient username

    Returns:
    Response with status 200 if message sent successfully. 
	Response with status 404 if recipient does not exist as a registered user.
	Response with status 404 if message missing recipient name. 

    Raises:
	None

     """

	username = request.user.username
	request.data._mutable = True
	request.data["sender"] = username
	request.data._mutable = False
	print(request.data)
	message = MessagesSerializer(data=request.data)

	# validating for recipient so that emails can only be sent to valid recipients
	if not User.objects.filter(username = request.data["receiver"]).exists():
		return Response( data="This recipient does not exist." ,status=status.HTTP_404_NOT_FOUND)
	
	else:


		if message.is_valid():
			message.save()
			return Response(message.data)
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)


#view sent messages
#This API is for testing purposes, and is not used in the application.
@login_required
@api_view(['GET'])
def view_sent_messages(request):
	""" Gets all non deleted messages sent by current user. 

    Args:
    GET request 

    Returns:
    JSON  Response of all non deleted sent messages with status 200. 
	Response with status 404 if recipient does not exist as a registered user.
	Response with status 404 if no messages found.
	
    Raises:
	None

     """

	username = request.user
	print(username)
	
	#Filter messages for messages sent by the current logged in user
	username = request.user
	items =  Messages.objects.filter(sender = username, sender_delete_status = False).all().values()


	# if items is empty return not found response
	if items:
		serializer = MessagesSerializer(items, many=True)
		return Response(serializer.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)

#view received messages
#This API is for testing purposes, and is not used in the application.
@login_required
@api_view(['GET'])
def view_received_messages(request):
	""" Gets all non deleted messages received by current user. 

    Args:
    GET request 

    Returns:
    JSON  Response of all non deleted received messages with status 200. 
	Response with status 404 if recipient does not exist as a registered user.
	Response with status 404 if no messages found.
	
    Raises:
	None

     """
	
	#Filter messages for messages received by the current logged in user
	username = request.user
	items =  Messages.objects.filter(receiver = username, receiver_delete_status = False).all().values()


	# if items is empty return not found response
	if items:
		serializer = MessagesSerializer(items, many=True)
		return Response(serializer.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)




#delete message
@login_required
@api_view(['POST'])
def delete_message(request):
	""" Delete a sent/received message for current user. 

    Args:
    POST request 

    Returns:
    Response with status 200 if message deleted successfully.
	Response with status 404 if no messages found.
	
    Raises:
	None

     """
	print(request.data)
	username = request.user.username
	record_id = request.data["id"]

	#check if the message record exists
	obj = Messages.objects.get(pk=record_id)
	if obj:
		#delete message from sentbox for current user
		if username == obj.sender:
			obj.sender_delete_status = True
		
		#delete message from inbox for current user
		if username == obj.receiver:
			obj.receiver_delete_status = True
		obj.save()

		return Response(status=status.HTTP_202_ACCEPTED)
	else:
	 	return Response(status=status.HTTP_404_NOT_FOUND)


#return inbox template 
@login_required
def inbox(request):
	""" Render inbox page as an HTTPResponse

    Args:
    GET request

    Returns:
    inbox.html page with received messages in context if there are any undeleted received messages. 
	inbox.html page with user's name in context if there are any undeleted received messages.
	
	
    Raises:
	None """

	username = request.user

	#Filter messages for messages received by the current logged in user
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

   


#return sentbox template
@login_required
def sentbox(request):
	""" Render sentbox page as an HTTPResponse

    Args:
    GET request

    Returns:
    sentbox.html page with received messages in context if there are any undeleted sent messages. 
	sentbox.html page with user's name in context if there are any undeleted sent messages.
	
	
    Raises:
	None """

	username = request.user
	print(username)

	#Filter messages for messages sent by the current logged in user
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


#return compose message template
@requires_csrf_token
def compose(request):
	""" Render compose page as an HTTPResponse

    Args:
    GET request

    Returns:
	compose.html page with user's name in context if there are any undeleted sent messages.
	
    Raises:
	None """
	c = {}
	template = loader.get_template('compose.html')
	context = {
    	'user': request.user }
	return HttpResponse(template.render(context, request))
