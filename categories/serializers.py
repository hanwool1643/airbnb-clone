from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__" # 다른 옵션 exclude = ("name", "kind") or fields = ("name", "kind") 
