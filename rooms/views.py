from django.http import HttpResponse


def see_all_rooms(request):
    return HttpResponse("see all rooms")
