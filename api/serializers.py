
from django.db.models import fields
from rest_framework import serializers
from .models import Messages



class MessagesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Messages
		fields = ('id','sender', 'receiver', 'title', 'body', 'sender_delete_status', 'receiver_delete_status')
