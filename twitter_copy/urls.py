from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('posts.urls')),
    url(r'^', include('rest_framework.urls', namespace='rest_framework')),

]
