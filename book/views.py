from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from book.models import BookInfo
from django.http import JsonResponse
import json

"""
############## 书籍视图 #####################
通过REST来实现对书籍的增删改查
查询所有书籍：GET books/                           查询数据库---序列化操作（转换为字典数据）---返回响应
    1.查询所有数据
    2.将查询结果进行遍历，转换为字典列表
    3.返回响应
增加一本书籍：POST books/                           JSON--->dict （反序列化操作）
    1.接收参数
    2.验证参数
    3.操作数据库，增加数据
    4.返回响应                                  obj----->dict 序列化操作

############### 详情视图 ##################
删除一本书籍：DELETE books/id/                     查询
    1.接收参数，查询数据                         
    2.操作数据库（删除）
    3.返回响应
修改一本书籍：PUT books/id/
    1.接收参数              对象
    2.查询指定数据            JSON/dict
    3.修改数据库中的数据                             反序列化
    4.返回响应                                        序列化
查询一本书籍：GET books/id/
    1.接收参数
    2.查询指定数据
    3.返回响应
"""

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
        # 新增后再将新增的数据返回回去
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