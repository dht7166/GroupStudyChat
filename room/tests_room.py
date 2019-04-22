from django.test import TestCase,Client
from django.contrib.auth.models import User
from .models import Room
import random
# Create your tests here.

class TestCreateRoom(TestCase):
    def setUp(self):
        username_prefix = 'user_'
        password_prefix = 'password_of_'
        email_suffix = '@somerandomdomain.com'
        for i in range(10):
            username = username_prefix + str(i)
            password = password_prefix + username
            email = username + email_suffix
            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=email)
            user.save()


    def testCreateRoomPrivate(self):
        c = Client()
        for user_number in [1,3,5]:
            username = 'user_'+str(user_number)
            password = 'password_of_'+username
            c.post('/homepage/login/', {'username': username, 'password': password})
            # Create a new room
            room_request = {'name':'Private room of '+username,
                            'description':'This room has private tag set to true',
                            'private':True,'invitation':''}
            c.post('/room/create_room/',room_request)

            # if everything went right, we should see a new room in the db.
            try:
                room = Room.objects.get(name='Private room of '+username)
                self.assertEqual(room.private,True,msg='Room that should be private has private tag false')
            except Room.DoesNotExist:
                self.assertTrue(False,msg='Room that was supposed to exist did not exist')


    def testCreateRoomPublic(self):
        c = Client()
        for user_number in [0,2,4]:
            username = 'user_'+str(user_number)
            password = 'password_of_' + username
            c.post('/homepage/login/', {'username': username, 'password': password})
            # Create a new room
            room_request = {'name': 'Public room of' +username,
                            'description': 'This room has private tag set to true',
                            'private': False, 'invitation': ''}
            c.post('/room/create_room/', room_request)

            # if everything went right, we should see a new room in the db.
            try:
                room = Room.objects.get(name='Public room of'+username)
                self.assertEqual(room.private, False, msg='Room that should be public has private tag true')
            except Room.DoesNotExist:
                self.assertTrue(False, msg='Room that was supposed to exist did not exist')

    def testCreateMultipleRoom(self):
        c = Client()
        for user_number in [6,7,8]:
            username = 'user_' + str(user_number)
            password = 'password_of_' + username
            c.post('/homepage/login/', {'username': username, 'password': password})
            room_name_prefix = 'Room_of_'+username+'_'
            for i in range(5):
                room_request = {'name': room_name_prefix+str(i),
                                'description': 'This is ' +username + ' '+ str(i)+' room',
                                'private': False, 'invitation': ''}
                c.post('/room/create_room/', room_request)

            # We created 5 rooms, there should now be 5 rooms that contain user_1 in its name.
            for i in range(5):
                try:
                    room = Room.objects.get(name=room_name_prefix+str(i))
                    self.assertEqual(room.private, False, msg='Room that should be public has private tag true')
                except Room.DoesNotExist:
                    self.assertTrue(False, msg='Room that was supposed to exist did not exist')

    def testCreateRoomMultipleUser(self):
        c = Client()
        # Let user 9 create a new room for multiple user
        username = 'user_9'
        password = 'password_of_'+username
        c.post('/homepage/login/', {'username': username, 'password': password})
        room_request_even = {'name': 'even',
                            'description': 'User with even number (except 9) goes in here',
                            'private': False, 'invitation': 'user_0,user_2,user_4,user_6,user_8'}
        room_request_odd = {'name': 'odd',
                            'description': 'User with odd number goes here',
                            'private': False, 'invitation':'user_1,user_3,user_5,user_7'}
        c.post('/room/create_room/',room_request_even)
        c.post('/room/create_room/', room_request_odd)
        even = Room.objects.get(name='even')
        odd = Room.objects.get(name='odd')
        for i in range(9):
            user = 'user_'+str(i)
            pwd = 'password_of_'+user
            c.get('/homepage/logout')
            c.post('/homepage/login/', {'username': user, 'password': pwd})
            # This guy should have access to certain room
            response = c.get('/room/'+str(even.id)+'/')
            if i%2==0:
                self.assertEqual(response.status_code,200)
            else:
                self.assertNotEqual(response.status_code,200)
            response = c.get('/room/'+str(odd.id)+'/')
            if i % 2:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertNotEqual(response.status_code, 200)





