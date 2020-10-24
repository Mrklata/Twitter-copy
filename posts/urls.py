from rest_framework import routers

from posts.api import CreatePostView, CreateWallView, CreatePostRatingView

router = routers.SimpleRouter()
router.register(r'posts', CreatePostView, basename='post')
router.register(r'wall', CreateWallView, basename='wall')
router.register(r'post-rating', CreatePostRatingView, basename='post-rating')
urlpatterns = router.urls
