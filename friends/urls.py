from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='imdex'),

    #API
    path('docs/', TemplateView.as_view(
        template_name='friends/docs.html',
        extra_context={'schema_url': 'openapi-schema-yaml'}
    ), name='swagger-ui'),
    path('api/v1/users', views.CustomUserCreate.as_view(), name='create_user'),
    path('api/v1/users/<int:pk>', views.CustomUserViewSet.as_view({'get': 'retrieve'}), name='get_user_info_by_id'),
    path('api/v1/users/<int:pk>/listOfFriends', views.CustomUserViewSet.as_view({'get': 'get_list_friends'}), name='get_list_of_friends_by_user_id'),
    path('api/v1/users/<int:pk>/listOfFriendRequests', views.CustomUserViewSet.as_view({'get': 'get_list_friend_requests'}), name='get_list_of_friend_requests_by_user_id'),
    path('api/v1/users/friendStatus/<int:firstpk>/<int:secondpk>', views.FriendStatus.as_view(), name='get_friend_status_between_users_by_user_id'),
    path('api/v1/users/<int:userpk>/relation/<int:friendpk>', views.DeleteRelation.as_view(), name='delete_user_from_friend_by_user_id'),
    path('api/v1/friendRequests/<int:fromuserpk>/<int:touserpk>', views.FriendRequestCreate.as_view(), name='send_friend_request_to_user_by_user_id'),
    path('api/v1/friendRequests/response/<int:requestpk>/<int:actionid>', views.FriendRequestResponse.as_view(), name='response_friend_request_by_request_id'),
]