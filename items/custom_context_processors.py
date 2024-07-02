from items.models import Category, Type


def home(request):
    return {
        'categories': Category.objects.all(),
        'types': Type.objects.all(),
    }
