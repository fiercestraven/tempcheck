import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Module

# Create your tests here.


def create_module(module_name, module_description):
    """
    Create a module with the given name and description.
    """
    name = 'test000'
    desc = 'test case module'
    return Module.objects.create(module_name=name, module_description=desc)


class ModuleIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('tcapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No modules are available.")
        self.assertQuerysetEqual(response.context['module_list'], [])

# fv - next steps: give modules an "active/inactive" attribute. Only display modules that are active. Test this. https://docs.djangoproject.com/en/4.1/intro/tutorial05/
# fv - after that, add a similar get_queryset method to ResultsView and create a new test class for that view.
# fv - then, Questions can be published on the site that have no Choices. So, our views could check for this, and exclude such Questions. Our tests would create a Question without Choices and then test that it’s not published, as well as create a similar Question with Choices, and test that it is published.
# fv - future tests might include making sure only pings in the relevant time frame are included. Make sure no pages are returning 404 that shouldn't be.
# fv - note - have a separate TestClass for each model or view, and a separate test method for each set of conditions you want to test