from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'chat_list', ChatList, basename='chat_list')
router.register(r'create_chat', CreateChatViewSet, basename='create_chat')
router.register(r'add_message', AddMessageViewSet, basename='add_message')
router.register(r'get_messages', GetMessages, basename='get_messages')
router.register(r'request_for_help', RequestForHelp, basename='RequestForHelp')
router.register(r'delete_message', DeleteMessageViewSet, basename='delete_message')
router.register(r'edit_message', EditMessageViewSet, basename='edit_message')





