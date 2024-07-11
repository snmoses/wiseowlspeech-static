from rest_framework import serializers
from .models import Article

class FieldQuillSerializer(serializers.Field):
    def to_representation(self, value):
        return value.html if hasattr(value, 'html') else str(value)


class ArticleSerializer(serializers.ModelSerializer):
    content = FieldQuillSerializer()

    class Meta:
        model = Article
        fields = ['title', 'content', 'author', 'created_at', 'published']
