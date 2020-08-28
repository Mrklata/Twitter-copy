from rest_framework import routers
from users.api import CreateUserView, CreateFriendRequestView

router = routers.SimpleRouter()
router.register(r'users', CreateUserView, basename='user')
router.register(r'friend_request', CreateFriendRequestView, basename='friend_request')
urlpatterns = router.urls
