import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from .models import Usr


def index(request):
    return JsonResponse({"message": "HELLO"})


@csrf_exempt
def auth(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # The user is authenticated, log them in
                if user.email_active:
                    login(request, user)
                    return JsonResponse({"message": "ok"})
                else:
                    return JsonResponse({"message":"email_activation","uuid":user.uuid})
            else:
                return JsonResponse({"error": "not_correct_login_pass"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "invalid_json"}, status=400)

    return JsonResponse({"error": "req_invalid"}, status=400)




def send_email_verification(email,username,uuid):
    pass

@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        # Check if a user with the same username exists
        if Usr.objects.filter(username=username).exists():
            return JsonResponse({"message": "usernamenotavailable"})
        
        # Check if a user with the same email exists
        if Usr.objects.filter(email=email).exists():
            return JsonResponse({"message": "emailnotavailable"})
        
        # Create a new user
        user = Usr.objects.create(username=username, email=email, password=password)
        user.save()
        
        login(request,user)        
        return JsonResponse({"message": "ok"})
        
    else:
        return JsonResponse({"message": "notpostmethod"})
    
    return JsonResponse({"message": "error"})


@csrf_exempt
def get_user(request):
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({"message": "notauth"})

    user_data = {
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "avatar": user.avatar.url if user.avatar else None,
        "id": user.pk,
        "created_At": user.created_At,
        "role": user.role,
        "desc": user.desc,
    }
    return JsonResponse(user_data, safe=False)
@csrf_exempt
def logoutpage(request):
    logout(request)

    return redirect('/')