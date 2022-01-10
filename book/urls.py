from django.urls import path
from book import views
urlpatterns = [
    path('books/',views.BookListView.as_view()),
    path('books/<int:pk>/', views.BookDetailView.as_view()),

    path('apibooks/', views.BookListAPIView.as_view()),
    path('genericbooks/', views.BookInfoGenericAPIView.as_view()),

]