from django.http import HttpResponseRedirect


def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/api-auth/login/?next=/api/v1/pokemon/')