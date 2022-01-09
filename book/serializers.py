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
# 隐藏的外键
class PeopleForeignSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    password = serializers.CharField()
    # description = serializers.CharField()
    # is_delete = serializers.BooleanField()

"""
{
    'id': 1, 'name': '射雕英雄传', 'pub_date': '1980-05-01', 'readcount': 12, 
    'people': [
                    OrderedDict([('id', 1), ('name', '郭靖'), ('password', '12')]),
                     OrderedDict([('id', 2), ('name', '黄蓉'), ('password', '123456abc')]), 
                     OrderedDict([('id', 3), ('name', '黄药师'), ('password', '123456abc)]),
                      OrderedDict([('id', 4), ('name', '欧阳锋'), ('password', '123456abc')]), 
                     OrderedDict([('id', 5), ('name', '梅超风'), ('password', '123456abc')],
}
"""


class BookInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(write_only=True, max_length=10, min_length=5)
    pub_date = serializers.DateField(required=True)
    readcount = serializers.IntegerField(required=False)

    # 评论量
    commentcount = serializers.IntegerField(required=False)
    def validate_readcount(self, value):
        # 检测到数据没有问题 返回数据
        if value < 0:
            # raise Exception('阅读量不能为负数')  自己定义的异常
            # 系统抛除异常
            raise serializers.ValidationError('阅读量不能为负数')
        return value

    # 多个字段的验证 attrs其实为data 可以自定义
    def validate(self, attrs):
        # 字典用 data.get('key') 不容易出现异常
        commentcount = attrs.get('commentcount')
        readcount = attrs.get('readcount')
        if commentcount > readcount:
            raise serializers.ValidationError('评论量不能大于阅读量')
        if readcount < 0:
            raise serializers.ValidationError('阅读量不能小于0  22')
        return attrs

    def create(self, validated_data):
        # 解包传入的字典
        return BookInfo.objects.create(**validated_data)
    """
    如果我们的序列化器继承自Serializer，当调用序列化器的save方法的时候，会
    调用序列化器的create方法
    """
    # 隐藏的外键 需要单独定义一个类 一本书关联多个人物 级连关系的数据获取
    # 在测试反序列化的时候， 有下面的这一项测试数据不会成功
    # people = PeopleForeignSerializer(many=True)
    # email = serializers.EmailField()
    # uuid = serializers.UUIDField()


####### 定义任务模型对应的序列化器 ################
class PeopleInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    password = serializers.CharField()
    description = serializers.CharField()
    is_delete = serializers.BooleanField()

    # 对外键进行学习
    # 1.如果我们定义的序列化器外键字段类型为IntegerField那么，我们定义的序列化器字段名必须和数据库中的字段名字一致
    # 拿到外键关联 id 值
    # book_id = serializers.IntegerField()

    # 2.如果不想写book_id,希望的外键数据的key就是模型字段的名字，
    # 那么PrimaryKeyRelatedField就可以获取关联的数据的模型id值
    # 如果设置外键QuerySet在验证数据的时候，我们要告诉系统，在哪里匹配外键数据 下面两种都可以
    # 拿到外键关联 id 值
    # book = serializers.PrimaryKeyRelatedField(read_only=True)   # 意思就是不验证数据了
    # book = serializers.PrimaryKeyRelatedField(queryset=BookInfo.objects.all())  # 去哪里找外键数据

    # 3.如果我们期望获取外键关联的 字符串 的信息， 这个时候 我们可以使用 StringRelationField
    # 即__str__方法中的self.name 的信息
    # 拿到外键字符串中的信息
    # book = serializers.StringRelatedField()

    # 4.book = 关联的BookInfo的一个关联对象数据，如果我们期望 获得book关联的模型的所有数据 为    book = BookInfoSerializer()
    # book = BookInfo.objects.get(id=xxx)
    # book = BookInfoSerializer(instance=book).data
    # 等号右面的book为模型对象，等号左面 的为
    book = BookInfoSerializer()
    """
    { 
        'id': 1, 'name': '郭靖', 'password': '123456abc', 'description': '降龙十八掌', 'is_delete': False,
         'book': OrderedDict(
            [('id', 1), ('name', '射('pub_date', '1980-05-01'), ('readcount', 12)]
         )
     }
    """

"""
1.book:1---PrimaryKeyRelationField
2.book_id:1---IntegerField
3.book:射雕英雄转---StringRelationField
4.book:{id:1, name:射雕英雄转, readcount:10}---BookInfoSerializer

"""




