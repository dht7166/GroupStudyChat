from django.test import TestCase,Client
from django.contrib.auth.models import User
from room.models import Room
# Create your tests here.

class RegisterTest(TestCase):
    def setUp(self):
        # Create 10 new normal users
        username_prefix = 'user_'
        password_prefix = 'password_of_'
        email_suffix = '@somerandomdomain.com'
        for i in range(10):
            username = username_prefix + str(i)
            password = password_prefix + username
            email = username+email_suffix
            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=email)
            user.save()

        # Create a superuser
        user = User.objects.create_superuser(username='admin',
                                             password = 'admin',
                                             email = 'admin@example.com')
        user.save()

    def testCreation(self):
        for i in range(10):
            try:
                username = 'user_'+str(i)
                user = User.objects.get(username=username)
                self.assertEqual(user.username,username)
            except User.DoesNotExist:
                # User definately exist, in that case our db is wrong
                self.assertTrue(False,msg='User that definately exist was reported as non exist')

        for i in range(10,15):
            # User definately does not exist
            with self.assertRaises(User.DoesNotExist,msg='User that should not exist was reported as exist'):
                username = 'user_'+str(i)
                user = User.objects.get(username=username)

    def testCorrectLoginLogout(self):
        c = Client()
        for i in range(10):
            # Test log in and log out for each of the 10 normal users
            response = c.get('/room/lobby/')
            self.assertEqual(response.status_code,302,msg='Did not redirect anonymous user')
            username = 'user_'+str(i)
            password = 'password_of_'+username
            c.post('/homepage/login/',{'username':username,'password':password})
            response = c.get('/room/lobby/')
            self.assertEqual(response.status_code, 200,msg='authenticated user cannot access lobby page')
            c.get('/homepage/logout/')

    def testAdminLogin(self):
        c = Client()
        for i in range(10):
            # normal user cannot log in into admin site
            response = c.get('/admin/')
            self.assertEqual(response.status_code,302,msg='unauthenticated request can access admin page')
            username = 'user_'+str(i)
            password = 'password_of_'+username
            c.post('/homepage/login/',{'username':username,'password':password})
            response = c.get('/admin/')
            self.assertEqual(response.status_code, 302,msg = 'non-admin user can access admin page')
            c.get('/homepage/logout/')
        # Only admin will get a 200 reponse code
        username = 'admin'
        password = 'admin'
        c.post('/homepage/login/', {'username': username, 'password': password})
        response = c.get('/admin/')
        self.assertEqual(response.status_code, 200,msg='admin cannot access admin page')







