from django.urls import re_path
from . import views
from . import models

urlpatterns = [
    re_path(r'^movie_all/(?P<page>\d*)', views.whole_list, {'model': models.Movie}, name='whole_list'),
    re_path(r'^actor_all/(?P<page>\d*)', views.whole_list, {'model': models.Actor}, name='whole_list'),
    re_path(r'^movie_detail/(?P<id>.*)', views.detail, {'model': models.Movie}, name='movie_detail'),
    re_path(r'^actor_detail/(?P<id>.*)', views.detail, {'model': models.Actor}, name='actor_detail'),
    re_path(r'^search/(?P<item>.*)/(?P<query_string>.*)/(?P<page>\d*).*', views.search, name='search'),
    re_path(r'^seen/(?P<movie_id>.*)', views.seen, name='seen'),
    re_path(r'^add_seen/(?P<movie_id>.*)', views.add_seen, name='seen'),
    re_path(r'^expect/(?P<movie_id>.*)', views.expect, name='expect'),
    re_path(r'^add_expect/(?P<movie_id>.*)', views.add_expect, name='expect'),
    re_path(r'^search_suggest/(?P<query_string>.*)', views.search_suggest, name='search_suggest'),
]
