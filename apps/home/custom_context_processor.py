from apps.post.models import CategoryIndex
from apps.home.models import Author, Home


def get_navigation(request):
    home = Home.objects.first()
    navigation = []
    if home:
        navigation = home.get_children().live()

    return {"navigation": navigation}
