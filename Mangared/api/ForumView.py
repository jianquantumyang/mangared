from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Forum, WatchedForum, Comment2Forum
from urllib.parse import unquote
from django.http import JsonResponse
from .models import Forum,Manga
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



def get_forum(request):
    # Get the 'discussions' parameter from the URL and decode it
    discussions = request.GET.get("discussions", None)
    discussions = unquote(discussions) if discussions is not None else None

    # Fetch forum records filtered by the 'discussions' parameter if it is not None
    if discussions is not None:
        # Use a filter condition that makes sense for your use case
        # For example, if discussions is a string parameter you want to match against a field like 'theme':
        forums = Forum.objects.filter(theme__icontains=discussions)[:int(request.GET.get("limit", 10))]
    else:
        # If 'discussions' is None, retrieve all forum records
        forums = Forum.objects.all()[:int(request.GET.get("limit", 10))]

    forums_with_user_info = []

    for forum in forums:
        forum_info = {
            'forum_title': forum.forum_title,
            'forum_created_At': forum.created_At,
            'user_avatar': forum.usr.avatar.url,
            'user_username': forum.usr.username,
            'user_uuid': forum.usr.uuid,
            'forum_theme': forum.theme,
            'forum_uuid': forum.uuid,
        }
        forums_with_user_info.append(forum_info)

    # Return the forum data with user info as a JSON response
    return JsonResponse(forums_with_user_info, safe=False)
def get_comments_recursively(comment, depth=0):
    comment_data = {
        'user_uuid': comment.usr.uuid,
        'user': comment.usr.username,
        'avatar': comment.usr.avatar.url,
        'comment': comment.comment,
        'comment_uuid':comment.uuid,
        'created_At': comment.created_At,
        'depth': depth,
        'replies': [],
    }

    replies = Comment2Forum.objects.filter(parent_comment=comment)
    if replies:
        comment_data['replies'] = [get_comments_recursively(reply, depth + 1) for reply in replies]

    return comment_data





def forum_detail(request, uuid):
    try:
        forum = Forum.objects.get(uuid=uuid)
    except Forum.DoesNotExist:
        return JsonResponse({'error': 'Forum not found'}, status=404)

    watched_count = WatchedForum.objects.filter(forum=forum).count()

    comments = Comment2Forum.objects.filter(forum=forum, parent_comment=None)
    comments_list = [get_comments_recursively(comment) for comment in comments]

    forum_details = {
        'forum_title': forum.forum_title,
        'theme': forum.theme,
        'username': forum.usr.username,
        'uuid_user': forum.usr.uuid,
        'watched_count': watched_count,
        'comments': comments_list[::-1],
        'forum_text': forum.forum_text,
        'created_At': forum.created_At,
    }

    # Проверяем наличие информации о манге
    if forum.manga:
        forum_details['manga_name'] = forum.manga.name
        forum_details['manga_image'] = forum.manga.img.url
        forum_details['manga_name_en'] = forum.manga.name_en
        forum_details['manga_original'] = forum.manga.name_original
        forum_details['manga_uuid'] = forum.manga.uuid
    return JsonResponse(forum_details)




def getLastForums(request):

    forums = Forum.objects.order_by('-created_At').values(
        'forum_title',
        'uuid',
        'theme',
        'created_At',
        'usr__uuid',
        'usr__avatar',
        'usr__username'
    )[:6]

    return JsonResponse(list(forums), safe=False)






@login_required
@csrf_exempt
def create_forum_post(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)

            # Extract data from the JSON object
            forum_title = data.get('topicHeader')
            forum_text = data.get('markdownContent')
            theme = data.get('topicTitle')
            selected_manga = data.get('selectedManga')
            manga = Manga.objects.get(uuid=selected_manga)
            print(data)

            # Create a new forum post
            if selected_manga!=None:
                new_forum_post = Forum(
                    usr=request.user,
                    forum_title=forum_title,
                    forum_text=forum_text,
                    theme=theme,
                    manga=manga
                )
            else:
                new_forum_post = Forum(
                    usr=request.user,
                    forum_title=forum_title,
                    forum_text=forum_text,
                    theme=theme,
                )
            new_forum_post.save()

            return JsonResponse({'message': 'Forum post created successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'This view only supports POST requests for authenticated users'})
    









def watchForum(request, uuid):
    if request.user.is_authenticated:
        forum = get_object_or_404(Forum, uuid=uuid)
        new_watch, created = WatchedForum.objects.get_or_create(forum=forum, usr=request.user)
        # Дальнейшая обработка, если нужно

        return JsonResponse({"message":"ok"})
    return JsonResponse({"message":"error"})





@login_required
@csrf_exempt
def commentAdd(request):

    if request.method == "POST":
        
        
        data = json.loads(request.body)
        if len(data.get('comment'))>3:
            forum = Forum.objects.get(uuid=data.get('uuid'))
            Comment2Forum.objects.create(usr=request.user,comment=data.get('comment'),forum=forum).save()

            return JsonResponse({"message":"ok"})
        else:
            return JsonResponse({"messsage":"short_comment"})


    return JsonResponse({"message":"error"})

