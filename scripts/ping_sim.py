# demo script to mimic ping submission for a lecture

# https://django-extensions.readthedocs.io/en/latest/runscript.html#

from tcapp.models import Module, Ping
from datetime import datetime
from time import sleep
from django.utils import timezone

def run():
    # Fetch modules
    modules = Module.objects.all()

    # print out module options and take in user input
    print("Which module would you like to select?")
    for idx, module in enumerate(modules, start=1):
        # 2d ensures padding for 2 digits
        print(f'  {idx:2d}. {module.module_shortname}')

    idx = int(input("Select a module: "))
    module = modules[idx - 1]

    print(f"You've selected module {module.module_shortname}")

    # print out lecture options and take in user input
    lectures = module.lecture_set.all()
    print("Which lecture would you like to select?")
    for idx, lecture in enumerate(lectures, start=1):
        # 2d ensures padding for 2 digits
        print(f'  {idx:2d}. {lecture.lecture_name}')

    idx = int(input("Type the name of the lecture: "))
    lecture = lectures[idx -1]

    print(f"You've selected lecture {lecture.lecture_name}")

    # get student modules
    student_modules = module.student_module_set.all()

    print(f'Generating pings...')

    # loop through all students in a given module and submit a ping for each
    for idx, student_module in enumerate(student_modules, start=1):
        student = student_module.student
        Ping(ping_date=datetime.now(timezone.utc), lecture=lecture, student=student).save()
        # put it an \a alert to add audible component
        print(f' [{idx}/{len(student_modules)}] {student.username} pinged!\a')
        sleep(3)