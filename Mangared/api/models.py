from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

class Usr(AbstractUser):
    
    uuid = models.UUIDField(db_index=True,default=uuid.uuid4,editable=False,primary_key=True)
    roles = [
        ("ADMIN", "ADMIN"),
        ("MODERATOR", "MODERATOR"),
        ("TRANSLATOR", "TRANSLATOR"),
        ("USER", "USER")
    ]
    email = models.EmailField(max_length=256, unique=True)
    avatar = models.ImageField(upload_to="avatar/%m/%d/",default="avatar/default.png")
    desc = models.TextField()
    created_At = models.DateTimeField(auto_now=True)
    role = models.CharField(choices=roles, max_length=20,default=roles[3][0])
    email_active = models.BooleanField(default=False)


    def __str__(self):
        return self.username


class Country(models.Model):
    country = models.CharField(max_length=64, verbose_name="Country")
    created_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country


class Genre(models.Model):
    genre = models.CharField(max_length=64, verbose_name="Genre")
    created_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.genre


class Manga(models.Model):
    seas = [('Зима','Зима'),('Весна','Весна'),('Осень','Осень'),('Лето','Лето')]
    type = [('Онгоинг','Онгоинг'),('Завершен','Завершен'),('Анонс','Анонс'),('Заморожен','Заморожен'),]
    
    name_en = models.CharField(max_length=512, verbose_name="Name in english")
    name = models.CharField(max_length=512, verbose_name="Manga_name")
    name_original = models.CharField(max_length=512, verbose_name="manga name in japan")
    status = models.CharField(max_length=16,choices=type)  
    
    
    season = models.CharField(max_length=12,choices=seas)  # 1,2,3,4
    year = models.IntegerField(verbose_name="Year Created at")
    created_At = models.DateTimeField(auto_now=True)
    
    author = models.CharField(max_length=64)
    company = models.CharField(max_length=64)
    
    country = models.ForeignKey(Country,on_delete=models.PROTECT)
    
    description = models.TextField()
    
    img = models.ImageField(upload_to="mangas/%Y/%m/%d/")
    genres = models.ManyToManyField(Genre)
    
    uuid = models.UUIDField(db_index=True,default=uuid.uuid4,editable=False,primary_key=True)

    def __str__(self):
        return self.name_en


class Rating_Manga(models.Model):
    rating = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    usr = models.ForeignKey(Usr, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.manga.name_en} - {self.rating}"


class Reading(models.Model):
    modes = [
        ("Читаю", "Читаю"),
        ("В планах", "В планах"),
        ("Прочитано", "Прочитано"),
        ("Брошено", "Брошено"),
        ("Отложено", "Отложено"),
    ]
    usr = models.ForeignKey(Usr, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    reading_mode = models.CharField(choices=modes, max_length=20)
    created_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usr.username} - {self.manga.name_en} ({self.reading_mode})"


class Likes(models.Model):
    usr = models.ForeignKey(Usr, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    created_At = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.usr.username} likes {self.manga.name_en}"
#null + true

class Translater(models.Model):
    usr = models.ForeignKey(Usr, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    created_At = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.usr.username} translates {self.manga.name_en}"

class Chapter(models.Model):
    uuid = models.UUIDField(db_index=True,default=uuid.uuid4,editable=False,primary_key=True)
    created_At = models.DateTimeField(auto_now=True)
    nameChapter = models.CharField(max_length=64)
    tom = models.IntegerField()
    glava = models.IntegerField()
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    translater = models.ForeignKey(Translater, on_delete=models.CASCADE)
    created_At = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.manga.name_en} - Chapter {self.nameChapter} (Tom {self.tom}, Glava {self.glava})"


class ChapterImages(models.Model):
    image = models.ImageField(upload_to="chimgs/%Y/%m/%d/")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    created_At = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.chapter.manga.name_en} - Chapter {self.chapter.nameChapter} - Image"




class Comment2Manga(models.Model):
    uuid = models.UUIDField(db_index=True,default=uuid.uuid4,editable=False,primary_key=True)


    comment = models.CharField(max_length=256)
    usr = models.ForeignKey(Usr, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    created_At = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Comment by {self.usr.username} on {self.manga.name_en}"


class Comment2Chapter(models.Model):
    uuid = models.UUIDField(db_index=True,default=uuid.uuid4,editable=False,primary_key=True)


    comment = models.CharField(max_length=256)
    usr = models.ForeignKey(Usr, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    created_At = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Comment by {self.usr.username} on Chapter {self.chapter.nameChapter} ({self.chapter.manga.name_en})"


class Forum(models.Model):
    theme_choice = [
        ('Поиск тайтлов','Поиск тайтлов'),
        ('Поиск команды','Поиск команды'),
        ('Поиск в команду','Поиск в команду'),
        ('Общение','Общение'),
        ('Обсуждение манги','Обсуждение манги'),
        ('Предложения для переводчиков','Предложения для переводчиков'),
        ('Предложения для сайта','Предложения для сайта'),
        ('Баги и проблемы','Баги и проблемы'),
    ]
    theme = models.CharField(max_length=32,choices=theme_choice,default=theme_choice[0][0])
    uuid = models.UUIDField(db_index=True,default=uuid.uuid4,editable=False,primary_key=True)
    manga = models.ForeignKey(Manga,on_delete=models.CASCADE,blank=True,null=True)
    usr = models.ForeignKey(Usr,on_delete=models.CASCADE)
    forum_title = models.CharField(max_length=50)
    forum_text = models.TextField()
    created_At = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.forum_title+" | " + self.theme




class Watched(models.Model):
    usr = models.ForeignKey(Usr,on_delete=models.CASCADE)
    created_At = models.DateTimeField(auto_now=True)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.usr.username + " | " + self.chapter.manga.name


class WatchedForum(models.Model):
    usr = models.ForeignKey(Usr,on_delete=models.CASCADE)
    created_At = models.DateTimeField(auto_now=True)
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE)

    
class Comment2Forum(models.Model):
    uuid = models.UUIDField(db_index=True,default=uuid.uuid4,editable=False,primary_key=True)

    created_At = models.DateTimeField(auto_now=True)
    usr = models.ForeignKey(Usr,on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return self.usr.username + " | " + self.forum.forum_title + " | comment "
