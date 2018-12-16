from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('post/<int:pk>', views.PostDetailView.as_view(), name="detail"),
    path('archives/<int:year>/<int:month>/', views.ArchivesView.as_view(), name='archives'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name="category"),
    path('post/author/<int:pk>/', views.AuthorPostView.as_view(), name="author_posts"),
    path('tag/<int:pk>/', views.TagView.as_view(), name="tag"),
    # 简单的搜索功能,如果使用需要更改 base.html 搜索的 name 应改为 keywords,
    # haystack默认为 q
    # path('search/', views.SearchView.as_view(), name='search'),
]
