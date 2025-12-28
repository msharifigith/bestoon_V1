from rest_framework import serializers
from web.models import income, out


class income_serializers(serializers.ModelSerializer):
    class Meta:
        model = income
        fields = '__all__'


class out_serializers(serializers.ModelSerializer):
    class Meta:
        model = out
        fields = '__all__'
