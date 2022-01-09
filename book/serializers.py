"""
DRF 框架可以帮助我们实现 序列化和反序列化的功能（对象和字典的相互转换）
BookInfo -----序列化器类---> 字典
豆子 -----豆浆机-----> 豆浆
序列化器类：
    1.将对象转换为字典
    2.序列化器类的定义
        2.1参考模型来定义

claass 序列化器名字（serializers.Serializer）
    字段名 = serializer.类型（选项）
    字段名字 和 模型字段名字一致
    字段的类型和模型的类型一致
"""
from rest_framework import serializers
from book.models import BookInfo

class BookInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    pub_date = serializers.DateField()
    readcount = serializers.IntegerField()

####### 定义任务模型对应的序列化器 ################
class PeopleInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    password = serializers.CharField()
    description = serializers.CharField()
    is_delete = serializers.BooleanField()

    # 对外键进行学习
    # 1.如果我们定义的序列化器外键字段类型为IntegerField那么，我们定义的序列化器字段名必须和数据库中的字段名字一致
    # book_id = serializers.IntegerField()

    # 2.如果不想写book_id,希望的外键数据的key就是模型字段的名字，
    # 那么PrimaryKeyRelatedField就可以获取关联的数据的模型id值
    # 如果设置外键QuerySet在验证数据的时候，我们要告诉系统，在哪里匹配外键数据 下面两种都可以
    # book = serializers.PrimaryKeyRelatedField(read_only=True)   # 意思就是不验证数据了
    book = serializers.PrimaryKeyRelatedField(queryset=BookInfo.objects.all())  # 去哪里找外键数据


