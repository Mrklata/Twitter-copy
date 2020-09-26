from rest_framework import routers
from users.api import CreateUserView, CreateFriendRequestView, CreateFriendResponseView


router = routers.SimpleRouter()
router.register(r'users', CreateUserView, basename='user')
router.register(r'friend_request', CreateFriendRequestView, basename='friend_request')
# router.register(r'friend_request/<int:id>', request_detail)
router.register(r'friend_response', CreateFriendResponseView, basename='friend-response')
urlpatterns = router.urls
