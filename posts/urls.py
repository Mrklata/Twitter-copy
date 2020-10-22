from rest_framework import routers

from posts.api import CreatePostView, CreateWallView

router = routers.SimpleRouter()
router.register(r'posts', CreatePostView, basename='post')
router.register(r'wall', CreateWallView, basename='wall')
urlpatterns = router.urls
