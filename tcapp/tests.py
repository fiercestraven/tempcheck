import datetime
import json
from rest_framework import status
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from .models import Module, User, Lecture, Reset, Ping, User_Module, Threshold
from .serializers import ModuleSerializer

# initialize the APIClient app
client = Client()

# set up sample data
def create_instructor_user(firstname, lastname, username, password):
    """
    Create an instructor user with the given info.
    """  
    return User.objects.create(first_name=firstname, last_name=lastname, username=username, password=password, is_staff=True)

def create_module(shortname, name, desc):
    """
    Create a module with the given name and description.
    """
    testinstructor = User.objects.create(first_name="Trina", last_name="Tester", username="ttester", password="test123")
    return Module.objects.create(module_shortname=shortname, module_name=name, module_description=desc, instructor=testinstructor, is_active=True)

def create_lecture(name, desc):
    """
    Create a lecture with the given name and description.
    """
    testinstructor = User.objects.create(first_name="Trina", last_name="Tester", username="ttester", password="test123")
    testmodule = Module.objects.create(module_shortname="CSCtest", module_name="Test Computing", module_description="This is a test module.", instructor=testinstructor, is_active=True)
    return Lecture.objects.create(lecture_name=name, lecture_description=desc, lecture_date=timezone.now(), module=testmodule)

def create_ping():
    """
    Create a ping with sample data.
    """  
    teststudent = User.objects.create(first_name="Sarah", last_name="Student", username="sstudent", password="test321")
    testmodule = Module.objects.create(module_shortname="CSCtest", module_name="Test Computing", module_description="This is a test module.", instructor=teststudent, is_active=True)
    testlecture = Lecture.objects.create(lecture_name="CSCtest_W1_L1", lecture_description="This is a test lecture.", lecture_date=timezone.now(), module=testmodule) 
    return User.objects.create(ping_date=timezone.now(), student=teststudent, lecture=testlecture)

def create_invalid_ping():
    """
    Create an invalid ping with no user data.
    """  
    teststudent = User.objects.create(first_name="Sarah", last_name="Student", username="sstudent", password="test321")
    testmodule = Module.objects.create(module_shortname="CSCtest", module_name="Test Computing", module_description="This is a test module.", instructor=teststudent, is_active=True)
    testlecture = Lecture.objects.create(lecture_name="CSCtest_W1_L1", lecture_description="This is a test lecture.", lecture_date=timezone.now(), module=testmodule) 
    return User.objects.create(ping_date=timezone.now(), lecture=testlecture)

def create_reset():
    """
    Create a reset with sample data.
    """  
    testinstructor = User.objects.create(first_name="Trina", last_name="Tester", username="ttester", password="test123")
    testmodule = Module.objects.create(module_shortname="CSCtest", module_name="Test Computing", module_description="This is a test module.", instructor=testinstructor, is_active=True)
    testlecture = Lecture.objects.create(lecture_name="CSCtest_W1_L1", lecture_description="This is a test lecture.", lecture_date=timezone.now(), module=testmodule) 
    return User.objects.create(reset_time=timezone.now(), instructor=testinstructor, lecture=testlecture)

def create_threshold():
    """
    Create a threshold with sample data.
    """  
    testinstructor = User.objects.create(first_name="Trina", last_name="Tester", username="ttester", password="test123")
    return User.objects.create(yellow_percentage=1.00, orange_percentage=2.00, red_percentage=3.00, instructor=testinstructor)

def create_usermodule():
    """
    Create a user-module data point with sample data.
    """  
    testuser = User.objects.create(first_name="Sarah", last_name="Student", username="sstudent", password="test321")
    testmodule = Module.objects.create(module_shortname="CSCtest", module_name="Test Computing", module_description="This is a test module.", instructor=testuser, is_active=True)
    return User.objects.create(module=testmodule, user=testuser)


# Tests
class GetAllModulesSuperuserTest(TestCase):
    """
    Test module for GET all modules API for a superuser
    """  
    def test_get_all_modules(self):
        # get API response
        response = client.get('http://localhost:8000/tcapp/api/modules/')
        # get data from db
        modules = Module.objects.all()
        serializer = ModuleSerializer(modules, many=True)
        # fv - line below isn't working
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetAllModulesInstructorUserTest(TestCase):
    """
    Test module for GET all modules API for an instructor user
    """  
    def test_get_all_instructor_modules(self):
        # define instructor
        instructor = create_instructor_user()
    # fv - log this person in somehow??
        # get API response
        response = client.get('http://localhost:8000/tcapp/api/modules/')
        # get data from db
        modules = Module.objects.all()
        serializer = ModuleSerializer(modules, many=True)
        # fv - queryset should be empty - could test against that, maybe?
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetAllPingsTest(TestCase):
    """
    Test module for GET all pings for a given lecture.
    """  

class CreateNewPingTest(TestCase):
    """
    Test module for POSTing a ping.
    """  
    def test_create_valid_ping(self):
        ping = create_ping()
        response = client.post(
            reverse('http://localhost:8000/tcapp/api/lectures/{ping.lecture_name}/pings/'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    def test_create_invalid_ping(self):
        invalid_ping = create_invalid_ping()
        response = client.post(
            reverse('http://localhost:8000/tcapp/api/lectures/{invalid_ping.lecture_name}/pings/'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
# class ModuleIndexViewTests(TestCase):
#     def test_no_modules(self):
#         """
#         If no modules exist, an appropriate message is displayed.
#         """
#         response = self.client.get('http://localhost:3000/modules')
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No modules to display.")
#         self.assertQuerysetEqual(response.context['module_list'], [])

    # def test_inactive_module_display(self):
    #     """
    #     Test that index displays an appropriate message if no active modules are available.
    #     """
    #     create_module(name="testmodule", desc="test", isactive=False)
    #     response = self.client.get(reverse('tcapp:index'))
    #     self.assertContains(response, "No modules to display.")

    # def test_active_module_display(self):
    #     """
    #     Test that module_list does contain an active module.
    #     """
    #     testmodule = create_module(name="testmodule", desc="test", isactive=True)
    #     response = self.client.get(reverse('tcapp:index'))
    #     self.assertQuerysetEqual(response.context['module_list'], [testmodule])


# https://docs.djangoproject.com/en/4.1/intro/tutorial05/
