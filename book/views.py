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
        # book_dict = json.loads(request.body.decode())
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

"""一级视图 查询所有书籍 增加一本书籍"""
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

"""
GenericAPIView 比 APIView扩展了一些属性和方法
属性
    queryset 设置查询结果集
    serializer_class 设置序列化器
    lookup_field = 'id'  设置查询指定数据的关键字参数
方法
    books = self.get_queryset()                             获取查询结果集
    serializer = self.get_serializer(instance=books, many=True)      获取序列化器实例
    book = self.get_object()                                获取指定的数据
"""
from rest_framework.generics import GenericAPIView
# 列表视图
class BookInfoGenericAPIView(GenericAPIView):
    # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器
    serializer_class = BookInfoModelSerializer

    def get(self, request):
        # 1.查询所有数据
        # books = BookInfo.objects.all()
        # books = self.queryset
        books = self.get_queryset()

        # 2.创建序列化器
        # serializer = BookInfoModelSerializer(books, many=True)
        # serializer = self.serializer_class(books, many=True)
        serializer = self.get_serializer(books, many=True)

        # 3.返回响应
        return Response(serializer.data)
    def post(self, request):
        # 1.接收数据
        data = request.data
        # 2.验证参数
        serializer = self.get_serializer(data=data)
        serializer.is_valid()
        # 3.保存数据
        serializer.save()
        return Response(serializer.data)

# 详情视图
class BookInfoDetailGenericAPIView(GenericAPIView):
    # 查询结果集---惰性，写了不会立即查询（这里查询所有数据即可）， 后续的代码可以采用 self.queryset.filter(id=pk)
    queryset = BookInfo.objects.all()
    # 设置序列化器
    serializer_class =BookInfoModelSerializer

    # 设置关键字参数的名字
    # lookup_field = 'id'
    def get(self, request, pk):
        # 1.查询指定数据
        # book = BookInfo.objects.get(id=pk)
        # 下面两种方案都可以
        # book = self.queryset.filter(id=pk)
        # book = self.get_queryset().filter(id=pk)
        book = self.get_object()
        # 2.将对象数据转换为字典数据
        serializer = self.get_serializer(instance=book)
        return Response(serializer.data)
        pass

    # 更新数据
    def put(self, request, pk):
        # 1.查询指定的数据
        book = self.get_object()
        # 2.接收参数，获取参数
        data = request.data
        # 3.验证参数
        serializer = self.get_serializer(instance=book, data=data)
        serializer.is_valid(raise_exception=True)
        # 4.更新数据
        serializer.save()
        # 5.返回响应
        return Response(serializer.data)
        pass

    def delete(self, request, pk):
        # 1.接收参数，查询数据
        book = self.get_object()
        # 2.操作数据库
        book.delete()
        # 3.返回响应
        from rest_framework import status
        return Response(status=status.HTTP_204_NO_CONTENT)
        pass
"""
二级视图与Mixin配合使用
"""
# 列表视图
from rest_framework.mixins import ListModelMixin, CreateModelMixin
class BookInfoGenericMixinAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器
    serializer_class = BookInfoModelSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


"""
详情视图
"""
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
class BookInfoDetailGenericMixinAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoModelSerializer
    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)
"""
三级视图
"""
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView
class BookInfoListCreateAPIView(ListCreateAPIView):
    # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器
    serializer_class = BookInfoModelSerializer

class BookInfoRetrieveUpdateDestroyAPIview(RetrieveUpdateDestroyAPIView):
    # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器
    serializer_class = BookInfoModelSerializer



from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView

"""
视图集 继承自APIView ----> APIView继承自View   也分3个等级！！！用的最多的是3级
如果我们把增删改查都方法哦一个视图集里，原则上是不行的！！！
为什么？？
因为一个类视图的http方法 不能重复
获取数据有 2个get get所有数据 get某一个数据
"""
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
# class BookViewSet(ViewSet):
#     def list(self, request):
#         pass
#     def create(self, request):
#         pass
#     def retrieve(self, request, pk=None):
#         pass
#     def update(self, request, pk=None):
#         pass
#     def partial_update(self, request, pk=None):
#         pass
#     def destroy(self, request, pk=None):
#         pass

class BookViewSet(ViewSet):
    # 获取所有的书籍 GET books/
    def list(self, request):
        queryset = BookInfo.objects.all()
        serializer = BookInfoModelSerializer(queryset, many=True)
        return Response(serializer.data)
    # 获取指定书籍 GET books/pk/
    def retrieve(self, request, pk=None):
        queryset = BookInfo.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = BookInfoModelSerializer(user)
        return Response(serializer.data)


"""
ModelViewSet
也可以理解为4级视图

兄弟 ReadOnlyModelViewSet
"""
from rest_framework.viewsets import ModelViewSet

# ModelViewSet的基本使用
class BookInfoModelViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoModelSerializer


"""
高级功能：
    1.概念
    2.配置
    3.效果
"""
from book.models import PeopleInfo
from book.serializers import PeopleInfoModelSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
# 系统为我们提供了两个分页类
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class PageNum(PageNumberPagination):
    # 开启分页的开关
    page_size = 5
    # 设置查询字符串的key，也相当于开关，只有设置了这个值，一页多少条记录才生效
    # page_size_query_param = 'page_size'
    page_size_query_param = 'ps'

    # 一页最多有多少条记录
    max_page_size = 5


# 人物视图集
class PeopleInfoModelViewSet(ModelViewSet):

    # 给视图单独设置权限
    # permission_classes = [AllowAny]
    # 单独设置分页类 需要重写来设置page_size
    pagination_class = PageNum
    # 下面的属性 和 重写的方法是相同的，具有相同的功效
    # queryset = PeopleInfo.objects.all()
    def get_queryset(self):
        return PeopleInfo.objects.all()

    # serializer_class = PeopleInfoModelSerializer
    def get_serializer_class(self):
        return PeopleInfoModelSerializer
















