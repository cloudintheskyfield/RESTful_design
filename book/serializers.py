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
    book_id = serializers.IntegerField()


