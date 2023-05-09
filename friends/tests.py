import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser, FriendRequest


client = Client()


class CreateNewCustomUser(TestCase):
    """ Test module for inserting a new User """

    def setUp(self):
        self.valid_payload = {
            'username': '1',
        }

        self.invalid_payload = '1'

        self.invalid_payload_2 = {
            'bad': '1',
        }

    def test_create_user(self):
        response = client.post(
            reverse('create_user'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_invalid_payload(self):
        response = client.post(
            reverse('create_user'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('create_user'),
            data=json.dumps(self.invalid_payload_2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_already_exist_error(self):
        client.post(
            reverse('create_user'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        response_2 = client.post(
            reverse('create_user'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response_2.content.decode('utf-8')), {"username": ["User with this username already exists."]})


class GetCustomUserInfo(TestCase):
    """ Test module for get User info by id """

    def setUp(self):
        self.valid_payload = ['test', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id']]

    def test_get_user_info(self):
        response = client.get(reverse('get_user_info_by_id', args=[self.valid_payload[1]]), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_info_auth_error(self):
        response = client.get(reverse('get_user_info_by_id', args=[self.valid_payload[1]]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'detail': 'Authentication credentials were not provided.'})

    def test_get_user_info_user_not_exist_error(self):
        response = client.get(reverse('get_user_info_by_id', args=[self.valid_payload[1]+1]), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'detail': 'Not found.'})


class GetListOfFriendsByUserId(TestCase):
    """ Test module for get User list of friends by id """

    def setUp(self):
        self.valid_payload = ['test', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id']]

    def test_get_user_friends(self):
        response = client.get(reverse('get_list_of_friends_by_user_id', args=[self.valid_payload[1]]), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_friends_auth_error(self):
        response = client.get(reverse('get_list_of_friends_by_user_id', args=[self.valid_payload[1]]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'detail': 'Authentication credentials were not provided.'})

    def test_get_user_friends_user_not_exist_error(self):
        response = client.get(reverse('get_list_of_friends_by_user_id', args=[self.valid_payload[1]+1]), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'User not exist'})


class GetListOfFriendRequestsByUserId(TestCase):
    """ Test module for get User list of friend requests by id """

    def setUp(self):
        self.valid_payload = ['test', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id'], 'test2', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test2'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id']]

    def test_get_user_requests(self):
        response = client.get(reverse('get_list_of_friend_requests_by_user_id', args=[self.valid_payload[1]]), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_requests_auth_error(self):
        response = client.get(reverse('get_list_of_friend_requests_by_user_id', args=[self.valid_payload[1]]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'detail': 'Authentication credentials were not provided.'})

    def test_get_user_requests_not_current_error(self):
        response = client.get(reverse('get_list_of_friend_requests_by_user_id', args=[self.valid_payload[1]]), headers={'X-USERNAME': self.valid_payload[2]})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'You haven`t permissions'})


class GetFriendStatusBetweenTwoUsers(TestCase):
    """ Test module for get friend status between two users """

    def setUp(self):
        self.valid_payload = ['test', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id'], 'test2', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test2'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id']]

    def test_get_friend_status(self):
        response = client.get(reverse('get_friend_status_between_users_by_user_id', args=(self.valid_payload[1], self.valid_payload[3],)), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode('utf-8')), {'status': 'nothing'})

    def test_get_friend_status_auth_error(self):
        response = client.get(reverse('get_friend_status_between_users_by_user_id', args=(self.valid_payload[1], self.valid_payload[3],)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'detail': 'Authentication credentials were not provided.'})

    def test_get_friend_status_not_request_user_error(self):
        response = client.get(reverse('get_friend_status_between_users_by_user_id', args=(self.valid_payload[3], self.valid_payload[1],)), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'You haven`t permissions'})

    def test_get_friend_status_user_not_exist_error(self):
        response = client.get(
            reverse('get_friend_status_between_users_by_user_id', args=(self.valid_payload[1], self.valid_payload[3]+1,)),
            headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'User witch you search not exist'})

    def test_get_friend_status_self_friend_error(self):
        response = client.get(
            reverse('get_friend_status_between_users_by_user_id',
                    args=(self.valid_payload[1], self.valid_payload[1],)),
            headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'You can`t be friends with yourself'})


class DeleteUserFromFriends(TestCase):
    """ Test module for delete user from friends """

    def setUp(self):
        self.valid_payload = ['test', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id'], 'test2', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test2'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id']]
        CustomUser.objects.get(pk=self.valid_payload[1]).friends.add(CustomUser.objects.get(pk=self.valid_payload[3]))

    def test_delete_friend_ok(self):
        response = client.delete(reverse('delete_user_from_friend_by_user_id', args=(self.valid_payload[1], self.valid_payload[3],)), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_auth_error(self):
        response = client.delete(reverse('delete_user_from_friend_by_user_id', args=(self.valid_payload[1], self.valid_payload[3],)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'detail': 'Authentication credentials were not provided.'})

    def test_delete_not_current_user_error(self):
        response = client.delete(reverse('delete_user_from_friend_by_user_id', args=(self.valid_payload[3], self.valid_payload[1],)), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'You haven`t permissions'})

    def test_delete_self_friend_error(self):
        response = client.delete(
            reverse('delete_user_from_friend_by_user_id',
                    args=(self.valid_payload[1], self.valid_payload[1],)),
            headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'You can`t be friends with yourself'})

    def test_delete_user_with_id_not_exist_error(self):
        response = client.delete(
            reverse('delete_user_from_friend_by_user_id', args=(self.valid_payload[1], self.valid_payload[3]+1,)),
            headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'User witch you search not exist'})

    def test_delete_not_friends_error(self):
        CustomUser.objects.get(pk=self.valid_payload[1]).friends.remove(CustomUser.objects.get(pk=self.valid_payload[3]))
        response = client.delete(
            reverse('delete_user_from_friend_by_user_id', args=(self.valid_payload[1], self.valid_payload[3],)),
            headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'Not friends'})


class SendFriendRequest(TestCase):
    """ Test module for sending friend requests """

    def setUp(self):
        self.valid_payload = ['test', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id'], 'test2', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test2'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id']]

    def test_send_request_ok(self):
        response = client.post(reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[1], self.valid_payload[3],)), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_request_auth_error(self):
        response = client.post(reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[1], self.valid_payload[3],)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'detail': 'Authentication credentials were not provided.'})

    def test_send_request_not_current_user_error(self):
        response = client.post(reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[3], self.valid_payload[1],)), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'You haven`t permissions'})

    def test_send_request_self_friend_error(self):
        response = client.post(
            reverse('send_friend_request_to_user_by_user_id',
                    args=(self.valid_payload[1], self.valid_payload[1],)),
            headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'You can`t be friends with yourself'})

    def test_send_request_user_with_id_not_exist_error(self):
        response = client.post(
            reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[1], self.valid_payload[3]+1,)),
            headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'User witch you search not exist'})

    def test_send_request_already_friend_error(self):
        CustomUser.objects.get(pk=self.valid_payload[1]).friends.add(CustomUser.objects.get(pk=self.valid_payload[3]))
        response = client.post(
            reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[1], self.valid_payload[3],)),
            headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'You are already friends'})

    def test_already_send_error(self):
        client.post(
            reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[1], self.valid_payload[3],)),
            headers={'X-USERNAME': self.valid_payload[0]})
        response_2 = client.post(
            reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[1], self.valid_payload[3],)),
            headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response_2.content.decode('utf-8')),
                         {'message': 'You are send request already'})

    def test_auto_accept(self):
        client.post(
            reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[1], self.valid_payload[3],)),
            headers={'X-USERNAME': self.valid_payload[0]})
        response = client.post(
            reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[3], self.valid_payload[1],)),
            headers={'X-USERNAME': self.valid_payload[2]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'You are friends :)'})


class ResponseFriendRequest(TestCase):
    """ Test module for response friend request """

    def setUp(self):
        self.valid_payload = ['test', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id'], 'test2', json.loads(client.post(
            reverse('create_user'),
            data=json.dumps({'username': 'test2'}),
            content_type='application/json'
        ).content.decode('utf-8'))['id']]

    def test_response_ok_accept(self):
        client.post(
            reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[3], self.valid_payload[1],)),
            headers={'X-USERNAME': self.valid_payload[2]})
        request_id = FriendRequest.objects.get(sender=CustomUser.objects.get(pk=self.valid_payload[3]), recipient=CustomUser.objects.get(pk=self.valid_payload[1])).id
        response = client.post(reverse('response_friend_request_by_request_id', args=(request_id, 1,)), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode('utf-8')), {'message': 'accepted'})

    def test_response_ok_reject(self):
        client.post(
            reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[3], self.valid_payload[1],)),
            headers={'X-USERNAME': self.valid_payload[2]})
        request_id = FriendRequest.objects.get(sender=CustomUser.objects.get(pk=self.valid_payload[3]), recipient=CustomUser.objects.get(pk=self.valid_payload[1])).id
        response = client.post(reverse('response_friend_request_by_request_id', args=(request_id, 0,)), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode('utf-8')), {'message': 'rejected'})

    def test_response_action_not_exist_error(self):
        client.post(
            reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[3], self.valid_payload[1],)),
            headers={'X-USERNAME': self.valid_payload[2]})
        request_id = FriendRequest.objects.get(sender=CustomUser.objects.get(pk=self.valid_payload[3]), recipient=CustomUser.objects.get(pk=self.valid_payload[1])).id
        response = client.post(reverse('response_friend_request_by_request_id', args=(request_id, 3,)), headers={'X-USERNAME': self.valid_payload[0]})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content.decode('utf-8')), {'message': 'Action (must be 1-accept or 0-reject)'})

    def test_send_request_auth_error(self):
        client.post(
            reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[3], self.valid_payload[1],)),
            headers={'X-USERNAME': self.valid_payload[2]})
        request_id = FriendRequest.objects.get(sender=CustomUser.objects.get(pk=self.valid_payload[3]),
                                               recipient=CustomUser.objects.get(pk=self.valid_payload[1])).id
        response = client.post(reverse('response_friend_request_by_request_id', args=(request_id, 0,)))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'detail': 'Authentication credentials were not provided.'})

    def test_send_request_not_current_user_error(self):
        client.post(
            reverse('send_friend_request_to_user_by_user_id', args=(self.valid_payload[3], self.valid_payload[1],)),
            headers={'X-USERNAME': self.valid_payload[2]})
        request_id = FriendRequest.objects.get(sender=CustomUser.objects.get(pk=self.valid_payload[3]),
                                               recipient=CustomUser.objects.get(pk=self.valid_payload[1])).id
        response = client.post(reverse('response_friend_request_by_request_id', args=(request_id, 0,)), headers={'X-USERNAME': self.valid_payload[2]})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'message': 'You haven`t permissions'})
