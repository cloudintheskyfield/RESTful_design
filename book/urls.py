from django.urls import path
from book import views
urlpatterns = [
    path('books/',views.BookListView.as_view()),
    path('books/<int:pk>/', views.BookDetailView.as_view()),

    path('apibooks/', views.BookListAPIView.as_view()),
    # 二级视图
    path('genericbooks/', views.BookInfoGenericAPIView.as_view()),
    # 详情视图
    path('genericbooks/<pk>/', views.BookInfoDetailGenericAPIView.as_view()),

    # 二级视图与mixin配合使用
    path('mixinbooks/', views.BookInfoGenericMixinAPIView.as_view()),
    # 详情视图
    path('mixinbooks/<pk>', views.BookInfoDetailGenericMixinAPIView.as_view()),

    # 三级视图
    path('thirdbooks/', views.BookInfoListCreateAPIView.as_view()),


]