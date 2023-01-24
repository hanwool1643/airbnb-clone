from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "kind",
        )  # 다른 옵션:  __all__,   exclude = ("name", "kind") or fields = ("name", "kind")
