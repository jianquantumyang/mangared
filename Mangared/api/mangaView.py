
from django.utils import timezone
from datetime import timedelta
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import linebreaksbr  # Импорт фильтра linebreaksbr
from django.db.models import Count,Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import ChapterImages, Manga,Reading,Rating_Manga,Chapter,Likes,Watched,Genre,Country


def get_most_watched_mangas_last_week(request):
    # Calculate the date one week ago from the current date
    one_week_ago = timezone.now() - timezone.timedelta(days=1)

    # Retrieve the most watched mangas in the last week
    most_watched_mangas = Manga.objects.filter(
        chapter__watched__created_At__gte=one_week_ago
    ).annotate(watch_count=Count('chapter__watched')).order_by('-watch_count').values('uuid', 'name_en','name','img','country__country')[:int(request.GET["limit"])]
   
   


    







                    

    return JsonResponse(list(most_watched_mangas), safe=False)



def get_chapter_with_images(request, uuid):
    chapter = get_object_or_404(Chapter, uuid=uuid)
    images = ChapterImages.objects.filter(chapter=chapter)
    

    try:
        next_chapter = Chapter.objects.filter(
            manga=chapter.manga, created_At__gt=chapter.created_At
        ).order_by("created_At")[0]
        next_chapter_uuid = str(next_chapter.uuid)
    except IndexError:
        next_chapter_uuid = None

    chapter_data = {
        'uuid': chapter.uuid,
        'created_At': chapter.created_At,
        'nameChapter': chapter.nameChapter,
        'tom': chapter.tom,
        'glava': chapter.glava,
        'manga_name':chapter.manga.name,
        'manga_uuid':chapter.manga.uuid,
        'next_uuid':next_chapter_uuid,

        # Add other fields as needed
    }
    
    images_data = [
        {
            'image_url': image.image.url,
            'created_At': image.created_At,
        }
        for image in images
    ]
    response_data = {
        'chapter': chapter_data,
        'images': images_data,
    }
    
    return JsonResponse(response_data)





def manga_search(request):
    search_query = request.GET.get('search', '')
    manga_list = Manga.objects.filter(name__icontains=search_query).values('name', 'uuid')
    return JsonResponse(list(manga_list), safe=False)






def get_popular_mangas(request, time_interval):
    # Define time ranges based on the time interval
    now = timezone.now()
    if time_interval == 'month':
        start_date = now - timedelta(days=30)
    elif time_interval == 'week':
        start_date = now - timedelta(weeks=1)
    elif time_interval == 'day':
        start_date = now - timedelta(days=1)
    else:
        return JsonResponse({"error": "Invalid time interval"})

    popular_mangas = Manga.objects \
        .filter(likes__created_At__gte=start_date) \
        .annotate(total_likes=Count('likes')) \
        .order_by('-total_likes') \
        .values('uuid', 'name', 'country__country', 'total_likes','img')[:int(request.GET.get("limit", 10))]

    return JsonResponse({"mangas": list(popular_mangas)})
def get_monthly_popularity(request):
    return get_popular_mangas(request, 'month')

def get_weekly_popularity(request):
    return get_popular_mangas(request, 'week')


def get_daily_popularity(request):
    return get_popular_mangas(request, 'day')





def getMangas(request):
  return JsonResponse({"mangas":list(Manga.objects.all().values()[:int(request.GET["limit"])])})



def getMostHighRating(request):
  return JsonResponse({"mangas":list(Manga.objects.annotate(average_rating=Avg('rating_manga__rating')).order_by('-average_rating').values()[:int(request.GET["limit"])])})




def getChoiceRedaction(request):
  
      # Calculate the date for one week ago from the current date
    one_week_ago = timezone.now() - timezone.timedelta(days=7)

    # Filter Reading objects for the last week
    readings_last_week = Reading.objects.filter(created_At__gte=one_week_ago)

    # Group by manga and count the number of readings for each manga
    most_reading_mangas = readings_last_week.values('manga__uuid', 'manga__name_en','manga__name','manga__img','manga__country__country').annotate(read_count=Count('manga__uuid')).order_by('-read_count')

    # Return the top 10 most read mangas at week
    top_10_mangas = most_reading_mangas[:int(request.GET["limit"])]

    
    # print(top_10_mangas)
    return JsonResponse(list(top_10_mangas), safe=False)
def newMangas(reqeust):
  # print(list(Manga.objects.order_by('-created_At').values()[:int(reqeust.GET["limit"])]))
   return JsonResponse(list(Manga.objects.order_by('-created_At').values('name_en','name','country__country','year','img','uuid')[:int(reqeust.GET["limit"])]),safe=False)



def catalog(request):
  return JsonResponse({"f":123})




def get_first_chapter_of_manga(manga_uuid):
    try:
        manga = Manga.objects.get(uuid=manga_uuid)
        first_chapter = Chapter.objects.filter(manga=manga).order_by('tom', 'glava').values().first()
        return first_chapter
    except Manga.DoesNotExist:
        return None




def get_similar_mangas(manga_instance, num_similar=5):
    # Get the genres of the input manga
    input_manga_genres = manga_instance.genres.all()

    # Find other mangas with at least one common genre
    similar_mangas = Manga.objects.filter(genres__in=input_manga_genres) \
                                  .exclude(pk=manga_instance.pk) \
                                  .annotate(common_genre_count=Count('genres')) \
                                  .order_by('-common_genre_count', '-created_At').values('country__country','img','name','uuid')[:num_similar]

    return similar_mangas



def getManga(request, uuid):
    manga = Manga.objects.get(uuid=uuid)
    
    # Calculate the average rating and round it to two decimal places
    rating_aggregate = Rating_Manga.objects.filter(manga__uuid=uuid).aggregate(Avg('rating'))
    rating = round(rating_aggregate['rating__avg'], 2) if rating_aggregate['rating__avg'] is not None else None


    rated = False
    liked = False  # Initialize 'liked' as False by default
    folder = "null"
    reading = "null"
    if request.user.is_authenticated:  # Check if the user is authenticated
        # Check if the user has liked the manga
        liked = Likes.objects.filter(usr=request.user, manga=manga).exists()
        rated  = Rating_Manga.objects.filter(usr=request.user, manga=manga).exists()
        folder = Reading.objects.filter(usr=request.user,manga=manga)
        reading = folder.first().reading_mode if folder.exists() else "null"

    return JsonResponse({
       "uuid": manga.uuid,
       "name": manga.name,
       "name_en": manga.name_en,
       "name_original": manga.name_original,
       "year": manga.year,
       "season": manga.season,
       "country": manga.country.country,
       "created_At": manga.created_At,
       "genres": list(manga.genres.values()),
       "desc": linebreaksbr(manga.description),
       "author": manga.author,
       "company": manga.company,
       "img": manga.img.url,
       "rating": rating,
       "folder":reading,
       "similar": list(get_similar_mangas(manga_instance=manga)),
       "firstchapter": get_first_chapter_of_manga(manga_uuid=uuid),
       "status": manga.status,
       "likes": Likes.objects.filter(manga=manga).count(),
       "liked": liked,  # Include the 'liked' attribute in the response,
       "rated":rated
    }, safe=False)

@login_required
@csrf_exempt
def liked_usr(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the JSON data from the request body
            manga_uuid = data.get('uuid', None)  # Get the 'uuid' field from the JSON data

            if manga_uuid is None:
                return JsonResponse({'message': 'Missing or invalid UUID in request body'}, status=400)

            manga = get_object_or_404(Manga, uuid=manga_uuid)  # Retrieve the manga based on the uuid
            
            # Check if the user has already liked the manga
            existing_like = Likes.objects.filter(usr=request.user, manga=manga).first()
            
            if existing_like:
                # The user has already liked the manga, so remove the like
                existing_like.delete()
                return JsonResponse({'message': 'Like removed successfully'})
            else:
                # The user has not liked the manga, so add a like
                Likes.objects.create(usr=request.user, manga=manga)
                return JsonResponse({'message': 'Manga liked successfully'})
        
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data in request body'}, status=400)
    
    return JsonResponse({'message': 'Invalid request method'}, status=405)





@csrf_exempt  # Add this decorator to disable CSRF protection (for simplicity)
@login_required
def select_rating(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        manga_uuid = data.get('manga_uuid')
        rating = data.get('rating')
        print(data,manga_uuid,rating)
        # Assuming you have a Manga model with a UUID field and a Rating_Manga model
        try:
            manga = Manga.objects.get(uuid=manga_uuid)
        except Manga.DoesNotExist:
            return JsonResponse({'error': 'Manga not found'}, status=404)
        
        # Create or update the rating for the current user
        user = request.user
        if user.is_authenticated:
            try:
                

                obje = Rating_Manga.objects.filter(manga=manga,usr=user)
                if obje.exists():
                    obje.update(rating=rating)
                else:
                    ratin = Rating_Manga.objects.create(rating=rating, usr=user, manga=manga)
                    ratin.save()

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
            
            # Calculate the average rating for the manga (you can customize this logic)
            average_rating = Rating_Manga.objects.filter(manga=manga).aggregate(Avg('rating'))['rating__avg']
            
            return JsonResponse({'message': 'Rating selected successfully', 'average_rating': average_rating})
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Handle other HTTP methods or errors as needed
    return JsonResponse({'error': 'Invalid request'})






def watch(request, uuid):
    if request.user.is_authenticated:
        chapter = get_object_or_404(Chapter, uuid=uuid)
        new_watch, created = Watched.objects.get_or_create(chapter=chapter, usr=request.user)
        # Дальнейшая обработка, если нужно

        return JsonResponse({"message":"ok"})
    return JsonResponse({"message":"error"})









def manga_search(request):
    query = request.GET.get('q', '')  # Получаем поисковой запрос из GET-параметра 'q'

    # Выполняем поиск манги на основе запроса (в данном примере, ищем совпадения в name и description)
    if query!="":
        manga_results = Manga.objects.filter(
            name__icontains=query
        ).values('name', 'country__country', 'img','uuid')[:20]
    else:
        manga_results = []
    return JsonResponse(list(manga_results), safe=False)






def listGenre(request):
    return JsonResponse(list(Genre.objects.all().values()),safe=False)





def countrylist(request):
    return JsonResponse(list(Country.objects.all().values()),safe=False)






def catalog(request):
    return JsonResponse(list(Manga.objects.all().values('uuid','name','img','country__country')[:50]),safe=False)