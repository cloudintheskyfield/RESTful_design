from django.urls import path
from book import views
urlpatterns = [
    # # 书籍列表视图 查询所有图书 增加图书
    # path('books/',views.BookListView.as_view()),
    # # 书籍详情视图 查询单个图书 修改图书信息 删除图书
    # path('books/<int:pk>/', views.BookDetailView.as_view()),
    #
    # # APIView
    # path('apibooks/', views.BookListAPIView.as_view()),
    # # 二级视图
    # path('genericbooks/', views.BookInfoGenericAPIView.as_view()),
    # # 详情视图
    # path('genericbooks/<pk>/', views.BookInfoDetailGenericAPIView.as_view()),
    #
    # # 二级视图与mixin配合使用
    # path('mixinbooks/', views.BookInfoGenericMixinAPIView.as_view()),
    # # 二级视图 详情视图
    # path('mixinbooks/<pk>', views.BookInfoDetailGenericMixinAPIView.as_view()),
    #
    # # 三级视图
    # path('thirdbooks/', views.BookInfoListCreateAPIView.as_view()),
    # # 三级视图 详情视图
    # path('thirdbooks/<pk>/', views.BookInfoRetrieveUpdateDestroyAPIview.as_view()),
    #
    # # 视图集
    # path('viewsetbooks/', views.BookViewSet.as_view({'get': 'list'})),
    # path('viewsetbooks/<pk>', views.BookViewSet.as_view({'get': 'retrieve'}))
    #
]

"""
视图集的路由比较特殊，我们可以借助drf的router来实现
DefaultRouter 和 SimpleRouter 
共同点：都可以帮助视图集自动生成路由
不同点：
    DefaultRouter：http://127.0.0.1:8000/可以访问
    SimpleRouter：http://127.0.0.1:8000不可以访问 
"""
from rest_framework.routers import DefaultRouter, SimpleRouter

# 1.创建路由/router实例
router = DefaultRouter()
# 2.设置列表视图和详情视图的公共部分（不包括/）
# prefix        （路由）列表视图和详情视图的公共部分（前置代码，前缀）
#                   Router会生成2个路由，一个是列表视图的路由prefix，另外一个是详情视图的路由prefix/pk/
# viewset           视图集
# basename=None     给列表视图和详情视图的路由设置别名， 别的规格先不讲
#                    别名的规范是 列表视图是：basename-list，详情视图是：basename-detail
#                   因为别名的原因，所以basename不要重复，一般我们都是以prefix作为basename，因为prefix不会重复
#                   basename在前后端不分离的模版中使用的情况较多
router.register('abc', views.BookInfoModelViewSet, basename='abc')
# 3.将router生成的路由，追加到urlpatterns
# urlpatterns += router.urls


router.register('people', views.PeopleInfoModelViewSet, basename='people')
urlpatterns += router.urls












