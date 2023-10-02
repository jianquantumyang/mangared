from .models import Reading,Manga,Usr

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def add_to_reading_folder(request):
    if request.method == 'POST':
        try:
            # Получите данные из JSON-запроса
            data = json.loads(request.body)
            manga_uuid = data.get('manga_uuid')
            reading_mode = data.get('reading_mode')

            manga = Manga.objects.get(uuid=manga_uuid)
            # Найти объект чтения, связанный с пользователем и мангой
            reading, created = Reading.objects.get_or_create(usr=request.user, manga=manga)
            
            if created:
                # Если объект чтения был создан, это значит, что манга добавляется в папку в первый раз
                reading.reading_mode = reading_mode  # Установите режим чтения
                reading.save()  # Сохраните обновленный объект чтения
                response_data = {'status': 'success', 'message': 'Manga added to the reading folder.'}
            else:
                # Если объект чтения уже существует, это значит, что манга уже есть в папке
                # Тут можно обновить режим чтения, если это необходимо
                if reading.reading_mode != reading_mode:
                    reading.reading_mode = reading_mode
                    reading.save()
                response_data = {'status': 'info', 'message': 'Manga is already in the reading folder.'}
        except Manga.DoesNotExist:
            response_data = {'status': 'error', 'message': 'Manga not found.'}
        return JsonResponse(response_data, status=200)



@login_required
@csrf_exempt
def remove_from_reading_folder(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        manga_uuid = data.get('manga_uuid')
        
        try:
            manga = Manga.objects.get(uuid=manga_uuid)
            Reading.objects.filter(usr=request.user, manga=manga).delete()
            
            response_data = {'status': 'success', 'message': 'Manga removed from the reading folder.'}
        except Manga.DoesNotExist:
            response_data = {'status': 'error', 'message': 'Manga not found.'}
        return JsonResponse(response_data, status=200 )







def get_manga_data(manga):

    return {
        "uuid": manga.uuid,
        "country": manga.country.country,
        "img": manga.img.url[6:],
        "name": manga.name,
        # Add other manga fields you need
    }
 
# Modify your views to include manga data
@login_required
def reading(request):
    readings = Reading.objects.filter(usr=request.user, reading_mode="Читаю")

    data = []
    for reading in readings:
        manga_data = get_manga_data(reading.manga)
        
        reading_info = {
            "reading_mode": reading.reading_mode,
            "created_At": reading.created_At.strftime("%Y-%m-%d %H:%M:%S"),  # Example date formatting
            "manga": manga_data,
            
        }
        data.append(reading_info)


    res = {
        "data":data,
        "count":readings.count(),
        "reading_mode":"Читаю"
    }
    return JsonResponse(res, safe=False)



@login_required
def plans(request):
    plans_list = Reading.objects.filter(usr=request.user, reading_mode="В планах")

    data = []
    for plan in plans_list:
        manga_data = get_manga_data(plan.manga)
        plan_info = {
            "reading_mode": plan.reading_mode,
            "created_At": plan.created_At.strftime("%Y-%m-%d %H:%M:%S"),  # Example date formatting
            "manga": manga_data,
        }
        data.append(plan_info)

    res = {
        "data":data,
        "count":plans_list.count(),
        "reading_mode":"В планах"
    }
    return JsonResponse(res, safe=False)


@login_required
def watched(request):
    watched_list = Reading.objects.filter(usr=request.user, reading_mode="Прочитано")

    data = []
    for watched in watched_list:
        manga_data = get_manga_data(watched.manga)
        watched_info = {
            "reading_mode": watched.reading_mode,
            "created_At": watched.created_At.strftime("%Y-%m-%d %H:%M:%S"),  # Example date formatting
            "manga": manga_data,
        }
        data.append(watched_info)
    res = {
        "data":data,
        "count":watched_list.count(),
        "reading_mode":"Просмотрено"
    }
    return JsonResponse(res, safe=False)


@login_required
def abandoned(request):
    abandoned_list = Reading.objects.filter(usr=request.user, reading_mode="Брошено")

    data = []
    for abandoned in abandoned_list:
        manga_data = get_manga_data(abandoned.manga)
        abandoned_info = {
            "reading_mode": abandoned.reading_mode,
            "created_At": abandoned.created_At.strftime("%Y-%m-%d %H:%M:%S"),  # Example date formatting
            "manga": manga_data,
        }
        data.append(abandoned_info)
    res = {
        "data":data,
        "count":abandoned_list.count(),
        "reading_mode":"Брошено"
    }
    return JsonResponse(res, safe=False)


@login_required
def postponed(request):
    postponed_list = Reading.objects.filter(usr=request.user, reading_mode="Отложено")

    data = []
    for postponed in postponed_list:
        manga_data = get_manga_data(postponed.manga)
        postponed_info = {
            "reading_mode": postponed.reading_mode,
            "created_At": postponed.created_At.strftime("%Y-%m-%d %H:%M:%S"),  # Example date formatting
            "manga": manga_data,
        }
        data.append(postponed_info)


        
    res = {
        "data":data,
        "count":postponed_list.count(),
        "reading_mode":"Отложено"
    }
    return JsonResponse(res, safe=False)

