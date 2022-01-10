from rest_framework import serializers
from book.models import BookInfo
# from book.views import BookInfo   # 这两种导入的方法都可以
class BookInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = '__all__'
