from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import generics, viewsets, views, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .authentication import ExampleAuthentication
from .models import CustomUser, FriendRequest
from .serializers import UserWithFriendsSerializer, UserSerializer, FriendRequestSerializer


def index(request):
    return render(request, 'friends/index.html', {})


class CustomUserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [ExampleAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all()
    serializer_class = UserWithFriendsSerializer

    @action(detail=True, methods=['get'])
    def get_list_friends(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'User not exist'})
        serializer = self.serializer_class(user)
        return Response(status=status.HTTP_200_OK, data=serializer.data['friends'])

    @action(detail=True, methods=['get'])
    def get_list_friend_requests(self, request, pk):
        if request.user.id != pk:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'You haven`t permissions'})

        requests = FriendRequest.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        serializer = FriendRequestSerializer(requests, many=True, context={'user': request.user})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


def is_users_exist_for_relation(first, second):
    users = CustomUser.objects.all()
    try:
        first = users.get(pk=first)
    except CustomUser.DoesNotExist:
        first = None
    try:
        second = users.get(pk=second)
    except CustomUser.DoesNotExist:
        second = None
    if first is None or second is None:
        error_variables = []
        if first is None:
            error_variables.append('first')
        if second is None:
            error_variables.append('second')
        return False, error_variables
    else:
        return True, first, second


class FriendStatus(views.APIView):
    authentication_classes = [ExampleAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, firstpk, secondpk):
        if request.user.id != firstpk:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'You haven`t permissions'})
        if firstpk == secondpk:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'You can`t be friends with yourself'})
        get_users = is_users_exist_for_relation(firstpk, secondpk)
        if get_users[0]:
            first, second = get_users[1:]
            friend_requests = FriendRequest.objects.all()
            if first in second.friends.all() and second in first.friends.all():
                return Response(status=status.HTTP_200_OK, data={'status': 'friends'})
            elif (first, second) in [(i.sender, i.recipient) for i in friend_requests]:
                return Response(status=status.HTTP_200_OK, data={'status': 'outgoing request'})
            elif (second, first) in [(i.sender, i.recipient) for i in friend_requests]:
                return Response(status=status.HTTP_200_OK, data={'status': 'incoming request'})
            else:
                return Response(status=status.HTTP_200_OK, data={'status': 'nothing'})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'message': 'User witch you search not exist'})


class DeleteRelation(views.APIView):
    authentication_classes = [ExampleAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, userpk, friendpk):
        if request.user.id != userpk:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'You haven`t permissions'})
        if userpk == friendpk:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'You can`t be friends with yourself'})
        get_users = is_users_exist_for_relation(userpk, friendpk)
        if get_users[0]:
            first, second = get_users[1:]
            if first in second.friends.all() and second in first.friends.all():
                first.friends.remove(second)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Not friends'})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'message': 'User witch you search not exist'})


class FriendRequestCreate(views.APIView):
    authentication_classes = [ExampleAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, fromuserpk, touserpk):
        if request.user.id != fromuserpk:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'You haven`t permissions'})
        if fromuserpk == touserpk:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'You can`t be friends with yourself'})
        get_users = is_users_exist_for_relation(fromuserpk, touserpk)
        if get_users[0]:
            sender, recipient = get_users[1:]
            if sender in recipient.friends.all() or recipient in sender.friends.all():
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'message': 'You are already friends'})
            else:
                try:
                    FriendRequest.objects.create(sender=sender, recipient=recipient)
                    if auto_accept(sender, recipient):
                        return Response(status=status.HTTP_200_OK, data={'message': 'You are friends :)'})
                    else:
                        return Response(status=status.HTTP_201_CREATED)
                except IntegrityError:
                    return Response(status=status.HTTP_400_BAD_REQUEST,
                                    data={'message': 'You are send request already'})

        else:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'message': 'User witch you search not exist'})


def auto_accept(sender, recipient):
    if (sender, recipient) in [(i.sender, i.recipient) for i in FriendRequest.objects.all()] and (recipient, sender) in [(i.sender, i.recipient) for i in FriendRequest.objects.all()]:
        sender.friends.add(recipient)
        recipient.friends.add(sender)
        FriendRequest.objects.filter(sender__in=[sender, recipient], recipient__in=[sender, recipient]).delete()
        return True
    else:
        return False


class FriendRequestResponse(views.APIView):
    authentication_classes = [ExampleAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, requestpk, actionid):
        if requestpk not in [i.id for i in FriendRequest.objects.filter(Q(recipient=request.user))]:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'You haven`t permissions'})
        request = FriendRequest.objects.get(pk=requestpk)
        if actionid == 1:
            request.sender.friends.add(request.recipient)
            request.delete()
            return Response(status=status.HTTP_200_OK, data={'message': 'accepted'})
        if actionid == 0:
            request.delete()
            return Response(status=status.HTTP_200_OK, data={'message': 'rejected'})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'message': 'Action (must be 1-accept or 0-reject)'})
