from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from movie.models import *
from django.http import HttpResponse
import json

from movie.initializer import search_cache, search_index


def add_seen(request, movie_id):
    if request.is_ajax():
        history = Seen.objects.filter(movieid_id=movie_id, username=request.user.get_username())
        if len(history) == 0:
            movie = Popularity.objects.get(movieid_id=movie_id)
            weight = movie.weight
            movie.delete()
            new_record = Popularity(movieid_id=movie_id, weight=weight + 3)
            new_record.save()
            new_record = Seen(movieid_id=movie_id, username=request.user.get_username())
            new_record.save()
            return HttpResponse('1')
        else:
            history.delete()
            return HttpResponse('0')


def add_expect(request, movie_id):
    if request.is_ajax():
        history = Expect.objects.filter(movieid_id=movie_id, username=request.user.get_username())
        if len(history) == 0:
            movie = Popularity.objects.get(movieid_id=movie_id)
            weight = movie.weight
            movie.delete()
            new_record = Popularity(movieid_id=movie_id, weight=weight + 3)
            new_record.save()
            new_record = Expect(movieid_id=movie_id, username=request.user.get_username())
            new_record.save()
            return HttpResponse('2')
        else:
            history.delete()
            return HttpResponse('0')


@csrf_protect
def detail(request, model, id):
    items = []
    try:
        if model.get_name() == 'movie' and id != 'None':
            try:
                d = Popularity.objects.get(movieid_id=id)
                weight = d.weight
                d.delete()
                new_record = Popularity(movieid_id=id, weight=weight + 1)
                new_record.save()
            except:
                new_record = Popularity(movieid_id=id, weight=1)
                new_record.save()
            label = 'actor'
            object = model.objects.get(movieid=id)
            records = Act.objects.filter(movieid_id=id)
            if request.user.get_username() != '':
                seen_list = [str(x).split('|')[1] for x in
                             Seen.objects.filter(username=request.user.get_username())]
                expect_list = [str(y).split('|')[1] for y in
                               Expect.objects.filter(username=request.user.get_username())]
                if id in seen_list:
                    object.flag = 1
                if id in expect_list:
                    object.flag = 2
            for query in records:
                for actor in Actor.objects.filter(actorid=query.actorid_id):
                    items.append(actor)
        if model.get_name() == 'actor':
            label = 'movie'
            object = model.objects.get(actorid=id)
            records = Act.objects.filter(actorid_id=id)
            for query in records:
                for movie in Movie.objects.filter(movieid=query.movieid_id):
                    items.append(movie)
    except:
        return render(request, '404.html')
    return render(request, '{}_list.html'.format(label), {'items': items, 'number': len(items), 'object': object})


def whole_list(request, model, page):
    if page is None:
        return render(request, '404.html')
    page = int(page)
    objects = model.objects.all()
    total_page = len(objects) // 10
    if (len(objects) / 10 - len(objects) // 10) > 0:
        total_page += 1
    if page > total_page:
        return render(request, '404.html')
    pages = [x + 1 for x in range(total_page)]
    end = 10 * page if page != total_page else len(objects)
    result = objects[10 * (page - 1):end]
    data = {'items': result, 'number': len(objects), 'pages': pages, 'current_page': page, 'next_page': page + 1,
            'last_page': page - 1, 'page_number': total_page}
    if page == 1:
        del data['last_page']
    if page == total_page:
        del data['next_page']
    return render(request, '{}_list.html'.format(model.get_name()), data)


def search(request, pattern):
    pattern = pattern.replace("%20", " ")
    search_results = search_index.search(pattern)
    movies, actors = [], []
    for movieid in search_results[0]:
        movies.append(search_index.data_in_memory['movie_dict'].get(movieid))
    for actorid in search_results[1]:
        actors.append(search_index.data_in_memory['actor_dict'].get(actorid))
    return render(request, 'searchresult.html',
                  {'items1': movies, 'search1': pattern, 'number1': len(movies),
                   'items2': actors,
                   'search2': pattern, 'number2': len(actors)})


def search_suggest(request, query_string):
    result = search_cache.get(query_string)
    if result is not None:
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    movie_list, actor_list = [], []
    res = search_index.search_suggest(query_string)
    movies, actors = [], []
    for movieid in res[0]:
        movies.append(search_index.data_in_memory['movie_dict'].get(movieid))
    for actorid in res[1]:
        actors.append(search_index.data_in_memory['actor_dict'].get(actorid))
    if len(movies) > 3:
        for i in range(3):
            movie_list.append({'movieid': movies[i].movieid, 'poster': movies[i].poster, 'title': movies[i].title})
    else:
        num = 3 - len(movie_list) if len(movies) > 3 - len(movie_list) else len(movies)
        for i in range(num):
            movie_list.append({'movieid': movies[i].movieid, 'poster': movies[i].poster, 'title': movies[i].title})
    if len(actors) > 3:
        for i in range(3):
            actor_list.append({'actorid': actors[i].actorid, 'photo': actors[i].photo, 'name': actors[i].name})
    else:
        num = 3 - len(actor_list) if len(actors) > 3 - len(actor_list) else len(actors)
        for i in range(num):
            actor_list.append({'actorid': actors[i].actorid, 'photo': actors[i].photo, 'name': actors[i].name})
    result = {'movie': movie_list, 'actor': actor_list, 'text': query_string}
    search_cache.set(query_string, result)
    return HttpResponse(json.dumps(result, ensure_ascii=False))


@csrf_protect
def seen(request, movie_id):
    if request.POST:
        try:
            d = Seen.objects.get(username=request.user.get_username(), movieid_id=movie_id)
            d.delete()
        except:
            return render(request, '404.html')
    records = Seen.objects.filter(username=request.user.get_username())
    movies = []
    for record in records:
        movie_id = str(record).split('|')[1]
        movies.append(Movie.objects.get(movieid=movie_id))
    return render(request, 'seen.html', {'items': movies, 'number': len(movies)})


def expect(request, movie_id):
    if request.POST:
        try:
            d = Expect.objects.get(username=request.user.get_username(), movieid_id=movie_id)
            d.delete()
        except:
            return render(request, '404.html')
    records = Expect.objects.filter(username=request.user.get_username())
    movies = []
    for record in records:
        movie_id = str(record).split('|')[1]
        movies.append(Movie.objects.get(movieid=movie_id))
    return render(request, 'expect.html', {'items': movies, 'number': len(movies)})
