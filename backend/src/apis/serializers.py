from rest_framework import serializers
from .models import User,Strategy,Result

class userSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields ='__all__'


class strategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields ='__all__'


class resultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields ='__all__'