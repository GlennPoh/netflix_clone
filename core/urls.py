from unicodedata import name
from django.urls import include, path
from django.contrib import admin
from core.views import Home, MovieDetail, ProfileList, ProfileCreate, Watch, PlayMovie

app_name = 'core'

urlpatterns = [
    path('admin', admin.site.urls),
    path('', Home.as_view()),
    path('profile/', ProfileList.as_view(), name='profile_list'),
    path('profile/create/', ProfileCreate.as_view(), name='profile_create'),
    path('watch/<str:profile_id>/', Watch.as_view(), name='watch'),
    path('movie/detail/<str:movie_id>/', MovieDetail.as_view(), name='show_det'),
    path('movie/play/<str:movie_id>/', PlayMovie.as_view(), name='play')
]