# import datetime
from operator import truediv
from queue import Empty

from django.test import TestCase
# from django.utils import timezone
from django.urls import reverse

from .models import Module, Instructor

# Create your tests here
def create_instructor(firstname, lastname, username, password):
    """
    Create an instructor with the given info.
    """  
    return Instructor.objects.create(first_name=firstname, last_name=lastname, username=username, instructor_password=password)

def create_module(name, desc, isactive):
    """
    Create a module with the given name and description.
    """
    testinstructor = Instructor.objects.create(first_name="Trina", last_name="Tester", username="ttester", instructor_password="test123")
    return Module.objects.create(module_name=name, module_description=desc, instructor=testinstructor, is_active=isactive)

class ModuleIndexViewTests(TestCase):
    def test_no_modules(self):
        """
        If no modules exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('tcapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No modules to display.")
        self.assertQuerysetEqual(response.context['module_list'], [])

    def test_inactive_module_display(self):
        """
        Test that index displays an appropriate message if no active modules are available.
        """
        create_module(name="testmodule", desc="test", isactive=False)
        response = self.client.get(reverse('tcapp:index'))
        self.assertContains(response, "No modules to display.")

    def test_active_module_display(self):
        """
        Test that module_list does contain an active module.
        """
        testmodule = create_module(name="testmodule", desc="test", isactive=True)
        response = self.client.get(reverse('tcapp:index'))
        self.assertQuerysetEqual(response.context['module_list'], [testmodule])


# https://docs.djangoproject.com/en/4.1/intro/tutorial05/
