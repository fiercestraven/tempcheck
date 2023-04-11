import datetime
import json
import unittest
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from django.urls import reverse
from .models import Module, User, Lecture, Reset, Ping, User_Module, Threshold
from .serializers import ModuleSerializer

class APITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Users - 1 admin, 2 instructors (a, b), 5 students (a-e)
        cls.admin=User.objects.create(username="admin", is_superuser=True)
        cls.instructor_a=User.objects.create(username="instructor_a", is_staff=True)
        cls.instructor_b=User.objects.create(username="instructor_b", is_staff=True)
        cls.student_a=User.objects.create(username="student_a")
        cls.student_b=User.objects.create(username="student_b")
        cls.student_c=User.objects.create(username="student_c")
        cls.student_d=User.objects.create(username="student_d")
        cls.student_e=User.objects.create(username="student_e")

        # Modules - 2 taught by instructor_a (module_a, module_b), 1 taught by instructor_b (module_c)
        cls.module_a=Module.objects.create(module_shortname="module_a", instructor=cls.instructor_a)
        cls.module_b=Module.objects.create(module_shortname="module_b", instructor=cls.instructor_a)
        cls.module_c=Module.objects.create(module_shortname="module_c", instructor=cls.instructor_b)

        # Lectures - each module has 2 lectures
        for module in (cls.module_a, cls.module_b, cls.module_c):
         for n in (1, 2):
            Lecture.objects.create(
               module=module,
               lecture_name=f"{module.module_shortname}_lecture_{n}",
               lecture_description=f"Test lecture {n} for module {module.module_shortname}",
               lecture_date=datetime.date.today(),
            )
        
        # User_Modules/Enrollment - all students are enrolled in both modules a and b; no students are enrolled in module c
        for student in (cls.student_a, cls.student_b, cls.student_c, cls.student_d, cls.student_e):
           for module in (cls.module_a, cls.module_b):
              User_Module.objects.create(
                 module=module,
                 user=student,
              )

    # MODULE TESTS
    # test instructor sees modules they teach
    def test_instructors_see_own_modules(self):
       self.client.force_authenticate(user=self.instructor_a)
       response = self.client.get("http://localhost:8000/tcapp/api/modules/")
       self.assertEqual(response.status_code, status.HTTP_200_OK)

       modules = [module["module_shortname"] for module in response.data]
       self.assertSequenceEqual(modules, ["module_a", "module_b"])
    
    # test instructor doesn't see modules they do not teach
    def test_instructors_dont_see_other_modules(self):
       self.client.force_authenticate(user=self.instructor_a)
       response = self.client.get("http://localhost:8000/tcapp/api/modules/")
       self.assertEqual(response.status_code, status.HTTP_200_OK)

       modules = [module["module_shortname"] for module in response.data]
       self.assertNotIn("module_c", modules)

    # test student sees modules they are enrolled in
    def test_students_see_enrolled_modules(self):
       self.client.force_authenticate(user=self.student_a)
       response = self.client.get("http://localhost:8000/tcapp/api/modules/")
       self.assertEqual(response.status_code, status.HTTP_200_OK)

       modules = [module["module_shortname"] for module in response.data]
       self.assertSequenceEqual(modules, ["module_a", "module_b"])

    # test student doesn't see modules they are not enrolled in
    def test_students_dont_see_unenrolled_modules(self):
       self.client.force_authenticate(user=self.student_a)
       response = self.client.get("http://localhost:8000/tcapp/api/modules/")
       self.assertEqual(response.status_code, status.HTTP_200_OK)

       modules = [module["module_shortname"] for module in response.data]
       self.assertNotIn("module_c", modules)
    
    # test anonymous users see no modules
    def test_anonymous_users_see_no_modules(self):
       response=self.client.get("http://localhost:8000/tcapp/api/modules/")
       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test inacative modules are not included in the api response
    def test_inactive_modules_are_hidden(self):
        self.module_a.is_active=False
        self.module_a.save()

        # with instructor
        with self.subTest(who=self.instructor_a):
           self.client.force_authenticate(user=self.instructor_a)
           response = self.client.get("http://localhost:8000/tcapp/api/modules/")
           modules = [module["module_shortname"] for module in response.data]
           self.assertNotIn("module_a", modules)

        # with student
        with self.subTest(who=self.student_a):
           self.client.force_authenticate(user=self.student_a)
           response = self.client.get("http://localhost:8000/tcapp/api/modules/")
           modules = [module["module_shortname"] for module in response.data]
           self.assertNotIn("module_a", modules)


    # MODULE DETAIL TESTS
    # test module details are returned for a module an instructor teaches
    def test_module_details_instructor(self):
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get("http://localhost:8000/tcapp/api/modules/module_a/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("module_description", response.data)

    # test module details are NOT returned for a module an instructor does not teach
    def test_module_details_non_instructor(self):
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get("http://localhost:8000/tcapp/api/modules/module_c/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test module details are returned for a module a student is enrolled in
    def test_module_details_student(self):
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get("http://localhost:8000/tcapp/api/modules/module_a/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("module_description", response.data)

    # test module details are NOT returned for a module a student is not enrolled in
    def test_module_details_non_student(self):
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get("http://localhost:8000/tcapp/api/modules/module_c/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test anonymous users see no module details
    def test_anonymous_users_see_no_module_details(self):
       response=self.client.get("http://localhost:8000/tcapp/api/modules/module_a")
        #fv ask Dan - why is this a 301 redirect, while the other anonymous user call under modules is a 403 forbidden?
       self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)


    # LECTURE DETAIL TESTS
    # test lecture details are returned for a lecture in a module that an instructor teaches
    def test_lecture_details_instructor(self):
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get("http://localhost:8000/tcapp/api/lectures/module_a_lecture_1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("lecture_description", response.data)

