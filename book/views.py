from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from rest_framework import serializers

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
    
数据验证全都到序列化器中了
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


"""
我们的序列化器目的将对象转换为字典数据
"""
from book.serializers import BookInfoSerializer
# BookInfoSerializer(instance=对象, data=字典)
from book.models import BookInfo

# 1：模拟查询一个对象
book = BookInfo.objects.get(id=1)

# 2：实例化序列化器，将对象数据传递给序列化器
serializer = BookInfoSerializer(instance=book)

# 3：获取序列化器，将对象转换为字典的数据
serializer.data

############### 传递多个 ###########3
from book.models import BookInfo
# 1.获取所有书籍
books = BookInfo.objects.all()
# 2.实例序列化
serializer = BookInfoSerializer(instance=books, many=True)
# 3.获取序列化
serializer.data

"""
[
OrderedDict([('id', 1), ('name', '射雕英雄传'), ('pub_date', '1980-05-01'), ('readcount', 12)]), 
OrderedDict([('id', 2), ('name', '天龙八部'), e', '1986-07-24'), ('readcount', 36)]),
OrderedDict([('id', 3), ('name', '笑傲江湖'), ('pub_date', '1995-12-24'), ('readcount', 20)]), 
OrderedDict('id', 4), ('name', '雪山飞狐'), ('pub_date', '1987-11-11'), ('readcount', 58)])
]

"""
##### 外键的序列化器的定义 ################
from book.serializers import PeopleInfoSerializer
from book.models import PeopleInfo
# 1.模拟查询对象
person = PeopleInfo.objects.get(id=1)
# 2.创建序列化器
serializer = PeopleInfoSerializer(instance=person)
# 3.获取序列化
serializer.data



#######################      反序列化   ###################
"""
序列化器验证数据的第一种形式：
1.我们的数据类型，可以帮助我们在反序列化的时候，验证传入数据的类型
    例如：
        DateField需要满足YYY-MM-DD
        IntegerField需要满足整形
2.通过字段的选项来验证数据
    例如：CharField(max_length=10, min_length=1)
        IntegerField(max_value=10,min_value=1)
        required默认为true
        read_only：只用于序列化使用，反序列化的时候忽略该字段
        write_only：只用于反序列化使用，序列化的时候忽略该字段
3.如果我们的数据满足类型要求，又满足选项要求，我们如果需要对数据进行进一步验证的时候，可以实现以下方法：
    以validate_ 开头，接 字段名字 的方法
    例如：
        def validate_readcount(self, value):    value为字段对应的值
            
            return value
4.如果需要对多个字段中的数据进行验证，我们可以通过 validate方法，来实现
    attrs可以为自定义单词
    例如：
        def validate(self, attrs):
        # 字典用 data.get('key') 不容易出现异常
        commentcount = attrs.get('commentcount')
        readcount = attrs.get('readcount')
        if commentcount > readcount:
            raise serializers.ValidationError('评论量不能大于阅读量')
            return attrs
        
"""
from book.serializers import BookInfoSerializer
# 将字典转换为对象
# 1.模拟字典数据
data = {
    # 'id': '1',
    'name': '入dao门',
    'pub_date': '2020-1-1',
    'readcount': 19
}
# 2.创建序列化容器，将字典数据给序列化器
# BookInfoSerializer(instance, data)
# instance 用于序列化 data用于反序列化
serializer = BookInfoSerializer(data=data)
# 3.验证数据
# 验证数据，正确返回True，错误返回false, 有异常的化会抛除
serializer.is_valid(raise_exception=True)

# 4.获取对象

""" """
from book.models import BookInfo
# 1.模拟获取一个对象
book = BookInfo.objects.get(id=1)
# 2.创建序列化器
serializer = BookInfoSerializer(instance=book)
# 3.获取序列化的字典数据
serializer.data

"""反序列化数据验证"""
from book.serializers import BookInfoSerializer
# 1.模拟字典数据
data = {
    'name': 'django',
    'pub_date': '2022-1-9',
    'readcount': 100,
    'commentcount':99,
}
# 2.创建序列化器，将字典数据传递给序列化器 一定要传关键字 不能省略！
serializer = BookInfoSerializer(data=data)
# 3.验证数据
serializer.is_valid(raise_exception=True)
# 4.验证数据没有问题之后，就可以调用保存方法了
serializer.save()








