from apps.post.models import CategoryIndex
from apps.home.models import Author, HomePage


def get_navigation(request):
    home = HomePage.objects.first()
    navigation = []
    if home:
        navigation = home.get_children().live()

    return {"navigation": navigation}
