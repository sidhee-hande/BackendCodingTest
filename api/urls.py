from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [

	#APIs
	path('', views.ApiOverview, name='home'),
	path('deletemessage/', views.delete_message, name='delete_message'),
    path('sendmessage/', views.send_message, name='send-message'),
    path('viewsentmessages/', views.view_sent_messages, name='viewsentmessages'),
    path('viewreceivedmessages/', views.view_received_messages, name='viewreceivedmessages'),
    path("signup/", SignUpView.as_view(), name="signup"),


	  #PAGES
	path('inbox', views.inbox, name='inbox'),
    path('sentbox', views.sentbox, name='sentbox'),
    path('compose', views.compose, name='compose'),

	
]
