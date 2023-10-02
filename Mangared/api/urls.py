from django.urls import path
from . import views 
from . import mangaView
from . import ForumView
from . import FoldersView
urlpatterns = [
  path('',views.index),

  path('login/',views.auth),
  path('logout/',views.logoutpage),
  path('user/',views.get_user),
  path('manga/popular/month/',mangaView.get_monthly_popularity),
  path('manga/popular/week/',mangaView.get_weekly_popularity),
  path('manga/popular/day/',mangaView.get_daily_popularity),
  path('manga/get/<uuid:uuid>/',mangaView.getManga),
  path('chapter/get/<uuid:uuid>/',mangaView.get_chapter_with_images),

  path('manga/rating/',mangaView.getMostHighRating),

  path('manga/catalog/',mangaView.catalog),
  path('manga/mangas/',mangaView.getMangas),
  path('manga/choiceredaction/',mangaView.getChoiceRedaction),
  path('manga/mostWatched/',mangaView.get_most_watched_mangas_last_week),
  path('manga/newAdded/',mangaView.newMangas),
  path('manga/like/add/',mangaView.liked_usr),
  path('forum/watch/<uuid:uuid>/',ForumView.watchForum),
  path('chapter/watch/<uuid:uuid>',mangaView.watch),
  path('manga_search/',mangaView.manga_search),
  path('forum/comment/add/',ForumView.commentAdd),
  path('manga/rating/select/', mangaView.select_rating),


  path('forum/get/',ForumView.get_forum),
  path('forum/detail/<uuid:uuid>/',ForumView.forum_detail),

  path('manga/folder/add/', FoldersView.add_to_reading_folder, name='add-to-reading-folder'),
  path('manga/folder/remove/', FoldersView.remove_from_reading_folder, name='remove-from-reading-folder'),
  path('folder/reading/',FoldersView.reading),
  path('folder/plans/',FoldersView.plans),
  path('folder/watched/',FoldersView.watched),
  path('folder/abandoned/',FoldersView.abandoned),
  path('folder/postponed/',FoldersView.postponed),


  path('forum/last/',ForumView.getLastForums),
  path('forum/create/',ForumView.create_forum_post),
  path('register/',views.register),
  path('genres/',mangaView.listGenre),
  path('countrys/',mangaView.countrylist),
  path('catalog/',mangaView.catalog)

]