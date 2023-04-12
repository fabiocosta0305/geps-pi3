from django.test import TestCase


def tests(request):
    if 'segunda' in request.POST:
        for x in request.POST:
            print(request.POST['segunda'])

