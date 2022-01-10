from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from book.models import BookInfo
from django.http import JsonResponse
import json

# Create your views here.
class BookListView(View):
    """
    查询所有图书、增加图书
    """
    def get(self, request):
        """
        查询所有图书
        路由：GET /books/
        """
        queryset = BookInfo.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id': book.id,
                'name': book.name,
                'pub_date': book.pub_date
            })
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        """
        新增图书
        路由：POST /books/
        """
        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book = BookInfo.objects.create(
            name=book_dict.get('name'),
            pub_date=book_dict.get('pub_date')
        )

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        },safe=False)

class BookDetailView(View):
    """
    获取单个图书信息
    修改图书信息
    删除图书
    """
    def get(self, request, pk):
        """
        获取单个图书信息
        路由： GET  /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({},status=404)

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        })

    def put(self, request, pk):
        """
        修改图书信息
        路由： PUT  /books/<pk>
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({},status=404)

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book.name = book_dict.get('name')
        book.pub_date = book_dict.get('pub_date')
        book.save()

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        })

    def delete(self, request, pk):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({},status=404)

        book.delete()

        return JsonResponse({},status=204)

from rest_framework.views import APIView
"""
使用APIView来实现 列表视图的功能 即增删改查
"""
from rest_framework.views import APIView
from book.models import BookInfo
from book.serializers import BookInfoModelSerializer
from django.http import HttpRequest   # django
from django.http import HttpResponse    # django
from rest_framework.request import Request  # drf
from rest_framework.response import Response  # drf
from rest_framework import status  # drf
class BookListAPIView(APIView):
    def get(self, request):
        # django --- request.GET
        # drf --- request.query_params
        query_params = request.query_params

        # 1.查询所有数据
        book = BookInfo.objects.all()
        # 2.将查询结果集遍历，转换为字典列表（序列化）
        serializer = BookInfoModelSerializer(instance=book, many=True)
        # 3.返回响应
        # return JsonResponse({'code': 'get', 'books':serializer.data}) # django
        return Response(serializer.data, status=status.HTTP_200_OK)  # 非常的人性化


    def post(self, request):
        # django --- request.POST , request.body
        # dfs --- request.data
        # 1.获取参数
        data = request.data
        # 2.验证参数
        serializer = BookInfoModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # 3.保存数据
        serializer.save()
        # 4.返回响应
        # return JsonResponse({'code': 'post'})
        return Response(serializer.data)

