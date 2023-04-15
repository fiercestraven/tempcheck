import datetime
import unittest
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone

# for increasing time: https://github.com/spulec/freezegun
from freezegun import freeze_time
import datetime
from .models import Module, User, Lecture, Reset, Ping, User_Module, Threshold


class APITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Users - 1 admin, 2 instructors (a, b), 5 students (a-e)
        cls.admin = User.objects.create(username="admin", is_superuser=True)
        cls.instructor_a = User.objects.create(username="instructor_a", is_staff=True)
        cls.instructor_b = User.objects.create(username="instructor_b", is_staff=True)
        cls.student_a = User.objects.create(username="student_a")
        cls.student_b = User.objects.create(username="student_b")
        cls.student_c = User.objects.create(username="student_c")
        cls.student_d = User.objects.create(username="student_d")
        cls.student_e = User.objects.create(username="student_e")
        cls.student_f = User.objects.create(username="student_f")

        # Modules - 2 taught by instructor_a (module_a, module_b), 1 taught by instructor_b (module_c)
        cls.module_a = Module.objects.create(
            module_shortname="module_a", instructor=cls.instructor_a
        )
        cls.module_b = Module.objects.create(
            module_shortname="module_b", instructor=cls.instructor_a
        )
        cls.module_c = Module.objects.create(
            module_shortname="module_c", instructor=cls.instructor_b
        )

        # Lectures - each module has 2 lectures
        for module in (cls.module_a, cls.module_b, cls.module_c):
            for n in (1, 2):
                Lecture.objects.create(
                    module=module,
                    lecture_name=f"{module.module_shortname}_lecture_{n}",
                    lecture_description=f"Test lecture {n} for {module.module_shortname}",
                    lecture_date=datetime.date.today(),
                )

        # User_Modules/Enrollment - all students are enrolled in both modules a and b; no students are enrolled in module c
        for student in (
            cls.student_a,
            cls.student_b,
            cls.student_c,
            cls.student_d,
            cls.student_e,
            cls.student_f,
        ):
            for module in (cls.module_a, cls.module_b):
                User_Module.objects.create(
                    module=module,
                    user=student,
                )

    # PROFILE TESTS
    # profile API returns profile data if a user is logged in
    # fv - is there a way to test more specifically that student_a and instructor_a's info is being returned? Tests fail
    def test_profile_data_authenticated(self):
        with self.subTest(who=self.student_a):
            self.client.force_authenticate(user=self.student_a)
            response = self.client.get("/tcapp/api/profile/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("last_name", response.data)

        with self.subTest(who=self.instructor_a):
            self.client.force_authenticate(user=self.instructor_a)
            response = self.client.get("/tcapp/api/profile/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("last_name", response.data)

    # profile API does not return data if nobody is logged in
    def test_profile_data_unauthenticated(self):
        response = self.client.get("/tcapp/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("last_name", response.data)

    # MODULE TESTS
    # admin user can see all modules
    def test_admin_see_all_modules(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/tcapp/api/modules/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Module.objects.count(), len(response.data))

    # test instructor sees modules they teach
    def test_instructors_see_own_modules(self):
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get("/tcapp/api/modules/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        modules = [module["module_shortname"] for module in response.data]
        self.assertSequenceEqual(modules, ["module_a", "module_b"])

    # test instructor doesn't see modules they do not teach
    def test_instructors_dont_see_other_modules(self):
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get("/tcapp/api/modules/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        modules = [module["module_shortname"] for module in response.data]
        self.assertNotIn("module_c", modules)

    # test student sees modules they are enrolled in
    def test_students_see_enrolled_modules(self):
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get("/tcapp/api/modules/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        modules = [module["module_shortname"] for module in response.data]
        self.assertSequenceEqual(modules, ["module_a", "module_b"])

    # test student doesn't see modules they are not enrolled in
    def test_students_dont_see_unenrolled_modules(self):
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get("/tcapp/api/modules/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        modules = [module["module_shortname"] for module in response.data]
        self.assertNotIn("module_c", modules)

    # test anonymous users see no modules
    def test_anonymous_users_see_no_modules(self):
        response = self.client.get("/tcapp/api/modules/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test inacative modules are not included in the api response
    def test_inactive_modules_are_hidden(self):
        self.module_a.is_active = False
        self.module_a.save()

        # with instructor
        with self.subTest(who=self.instructor_a):
            self.client.force_authenticate(user=self.instructor_a)
            response = self.client.get("/tcapp/api/modules/")
            modules = [module["module_shortname"] for module in response.data]
            self.assertNotIn("module_a", modules)

        # with student
        with self.subTest(who=self.student_a):
            self.client.force_authenticate(user=self.student_a)
            response = self.client.get("/tcapp/api/modules/")
            modules = [module["module_shortname"] for module in response.data]
            self.assertNotIn("module_a", modules)

    # MODULE DETAIL TESTS
    # test admin user can see module details for all models
    def test_module_details_admin(self):
        self.client.force_authenticate(user=self.admin)

        # for module_a
        with self.subTest(who=self.admin):
            response = self.client.get("/tcapp/api/modules/module_a/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("module_description", response.data)

        # for module_c
        with self.subTest(who=self.admin):
            response = self.client.get("/tcapp/api/modules/module_c/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("module_description", response.data)

    # test module details are returned for a module an instructor teaches
    def test_module_details_instructor(self):
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get("/tcapp/api/modules/module_a/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("module_description", response.data)

    # test module details are NOT returned for a module an instructor does not teach
    def test_module_details_non_instructor(self):
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get("/tcapp/api/modules/module_c/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test module details are returned for a module a student is enrolled in
    def test_module_details_student(self):
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get("/tcapp/api/modules/module_a/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("module_description", response.data)

    # test module details are NOT returned for a module a student is not enrolled in
    def test_module_details_non_student(self):
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get("/tcapp/api/modules/module_c/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test anonymous users see no module details
    def test_anonymous_users_see_no_module_details(self):
        response = self.client.get("/tcapp/api/modules/module_a/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # LECTURE DETAIL TESTS
    # test admin user can see lecture details for any lecture in any module
    def test_lecture_details_admin(self):
        self.client.force_authenticate(user=self.admin)

        # module_a, lecture_2
        with self.subTest(who=self.admin):
            response = self.client.get("/tcapp/api/lectures/module_a_lecture_2/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("lecture_description", response.data)

        # module_c, lecture_1
        with self.subTest(who=self.admin):
            response = self.client.get("/tcapp/api/lectures/module_c_lecture_1/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("lecture_description", response.data)

    # test lecture details are returned for a lecture in a module that an instructor teaches
    def test_lecture_details_instructor(self):
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get("/tcapp/api/lectures/module_a_lecture_1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("lecture_description", response.data)

    # test lecture details are not returned for a lecture in a module that an instructor does not teach
    def test_lecture_details_not_instructor(self):
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get("/tcapp/api/lectures/module_c_lecture_1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test lecture details are returned for a lecture in a module that a student is enrolled in
    def test_lecture_details_student(self):
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get("/tcapp/api/lectures/module_a_lecture_1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("lecture_description", response.data)

    # test lecture details are not returned for a lecture in a module that a student is not enrolled in
    def test_lecture_details_not_student(self):
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get("/tcapp/api/lectures/module_c_lecture_1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test no lecture details are returned for an anonymous user
    def test_anonymous_users_see_no_lecture_details(self):
        response = self.client.get("/tcapp/api/lectures/module_a_lecture_1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # PING TESTS
    # test admin users can see all pings for a given lecture
    def test_admin_can_see_all_pings(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/tcapp/api/lectures/module_a_lecture_1/pings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ping.objects.count(), len(response.data))

    # test instructors can see all pings for a given lecture they teach
    def test_instructor_can_see_pings(self):
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get("/tcapp/api/lectures/module_a_lecture_1/pings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ping.objects.count(), len(response.data))

    # test instructor cannot submit a ping
    def test_instructor_cannot_submit_ping(self):
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get("/tcapp/api/lectures/module_a_lecture_1/pings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # attempt to submit a ping via POST
        response = self.client.post(
            "/tcapp/api/lectures/module_a_lecture_1/pings/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test students cannot see any pings
    def test_student_cannot_see_pings(self):
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get("/tcapp/api/lectures/module_a_lecture_1/pings/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test student can submit a ping for a lecture in a module they're enrolled in
    def test_student_can_submit_ping(self):
        self.client.force_authenticate(user=self.student_a)

        # submit ping with POST: https://www.django-rest-framework.org/api-guide/testing/
        response = self.client.post(
            "/tcapp/api/lectures/module_a_lecture_1/pings/",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, Ping.objects.count())

    # test student can't submit a ping for a lecture of a module they're not enrolled in
    def test_student_cannot_submit_ping(self):
        self.client.force_authenticate(user=self.student_a)

        # submit ping with POST: https://www.django-rest-framework.org/api-guide/testing/
        response = self.client.post(
            "/tcapp/api/lectures/module_c_lecture_1/pings/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test anon users can't see pings
    def test_anonymous_users_see_no_pings(self):
        response = self.client.get("/tcapp/api/lectures/module_a_lecture_1/pings/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test anon users can't submit a ping
    def test_anonymous_users_cannot_submit_ping(self):
        response = self.client.post("/tcapp/api/lectures/module_a_lecture_1/pings/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # RESET TESTS
    # test instructor can submit a reset for a lecture in a module they teach
    def test_instructor_can_submit_reset(self):
        self.client.force_authenticate(user=self.instructor_a)

        response = self.client.post(
            "/tcapp/api/lectures/module_a_lecture_1/resets/",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # test instructor cannot submit a reset for a lecture in a module they do not teach
    def test_instructor_cannot_submit_reset(self):
        self.client.force_authenticate(user=self.instructor_a)

        response = self.client.post(
            "/tcapp/api/lectures/module_c_lecture_1/resets/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test student can't submit a reset
    def test_student_cannot_submit_reset(self):
        self.client.force_authenticate(user=self.student_a)

        response = self.client.post(
            "/tcapp/api/lectures/module_a_lecture_1/resets/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test anon users can't submit a reset
    def test_anonymous_users_cannot_submit_reset(self):
        response = self.client.post(
            "/tcapp/api/lectures/module_a_lecture_1/resets/",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # LECTURE TEMPERATURE TESTS
    # anyone can query the lecture_temperature api for any lecture
    def test_lec_temp_access(self):
        # for an admin user
        with self.subTest(who=self.admin):
            self.client.force_authenticate(user=self.admin)

            # for lecture from module_a
            with self.subTest():
                response = self.client.get(
                    "/tcapp/api/lectures/module_a_lecture_1/temperature/"
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

            # for lecture from module_b
            with self.subTest():
                response = self.client.get(
                    "/tcapp/api/lectures/module_b_lecture_1/temperature/"
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

        # for an instructor
        with self.subTest(who=self.instructor_a):
            self.client.force_authenticate(user=self.instructor_a)

            # for lecture from module_a
            with self.subTest():
                response = self.client.get(
                    "/tcapp/api/lectures/module_a_lecture_1/temperature/"
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

            # for lecture from module_b
            with self.subTest():
                response = self.client.get(
                    "/tcapp/api/lectures/module_b_lecture_1/temperature/"
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

            # fv - below doesn't work because no students are enrolled in module_c so it causes a "division by 0" error. Ask Dan whether to care.
            # for lecture from module_c
            # with self.subTest():
            #     response = self.client.get(
            #         "/tcapp/api/lectures/module_c_lecture_1/temperature/"
            #     )
            #     self.assertEqual(response.status_code, status.HTTP_200_OK)

        # for a student
        with self.subTest(who=self.student_a):
            self.client.force_authenticate(user=self.student_a)

            # with lecture from module_a
            with self.subTest():
                response = self.client.get(
                    "/tcapp/api/lectures/module_a_lecture_1/temperature/"
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

            # with lecture from module_b
            with self.subTest():
                response = self.client.get(
                    "/tcapp/api/lectures/module_b_lecture_1/temperature/"
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

        # for an anonymous user
        with self.subTest(self):
            # with lecture from module_a
            with self.subTest():
                response = self.client.get(
                    "/tcapp/api/lectures/module_a_lecture_1/temperature/"
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

            # with lecture from module_b
            with self.subTest():
                response = self.client.get(
                    "/tcapp/api/lectures/module_b_lecture_1/temperature/"
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    # FUNCTIONALITY TESTS
    # test that the lecture temperature increases correctly in response to ping levels crossing the default thresholds (15%, 25%, 35%)
    def test_temperature_increase_default_thresholds(self):
        # check initial threshold level
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, response.data)

        # class size is 6; submit 1 ping to cross first threshold
        Ping.objects.create(
            ping_date=timezone.now(),
            lecture=Lecture.objects.get(lecture_name="module_a_lecture_1"),
            student=User.objects.get(username="student_a"),
        )

        # check new temp is equal to 1
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(1, response.data)

        # submit another ping to cross second threshold and then check temperature is equal to 2
        Ping.objects.create(
            ping_date=timezone.now(),
            lecture=Lecture.objects.get(lecture_name="module_a_lecture_1"),
            student=User.objects.get(username="student_a"),
        )

        # check new temp is equal to 2
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(2, response.data)

        # submit another ping to cross third threshold and then check temperature is equal to 3
        Ping.objects.create(
            ping_date=timezone.now(),
            lecture=Lecture.objects.get(lecture_name="module_a_lecture_1"),
            student=User.objects.get(username="student_a"),
        )

        # check new temp is equal to 3
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(3, response.data)

    # test temperature response with custom thresholds
    def test_temperature_increase_custom_thresholds(self):
        # create custom threshold level
        Threshold.objects.create(
            yellow_percentage=10.00,
            orange_percentage=50.00,
            red_percentage=80.00,
            instructor=User.objects.get(username="instructor_a"),
        )
        # check custom threshold initial level
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, response.data)

        # class size is 6; submit 1 ping to cross first threshold
        Ping.objects.create(
            ping_date=timezone.now(),
            lecture=Lecture.objects.get(lecture_name="module_a_lecture_1"),
            student=User.objects.get(username="student_a"),
        )

        # check new temp is equal to 1
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(1, response.data)

        # submit another 2 pings to cross second threshold and then check temperature is equal to 2
        Ping.objects.create(
            ping_date=timezone.now(),
            lecture=Lecture.objects.get(lecture_name="module_a_lecture_1"),
            student=User.objects.get(username="student_a"),
        )
        Ping.objects.create(
            ping_date=timezone.now(),
            lecture=Lecture.objects.get(lecture_name="module_a_lecture_1"),
            student=User.objects.get(username="student_a"),
        )

        # check new temp is equal to 2
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(2, response.data)

        # submit another 1 pings to bring total to 5 to cross third threshold and then check temperature is equal to 3
        Ping.objects.create(
            ping_date=timezone.now(),
            lecture=Lecture.objects.get(lecture_name="module_a_lecture_1"),
            student=User.objects.get(username="student_a"),
        )

        Ping.objects.create(
            ping_date=timezone.now(),
            lecture=Lecture.objects.get(lecture_name="module_a_lecture_1"),
            student=User.objects.get(username="student_a"),
        )

        # check new temp is equal to 3
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(3, response.data)

    # test that temperature automatically resets after 3 minutes have passed
    def test_temperature_decreases_with_time(self):
        # check initial threshold level
        lecture = Lecture.objects.get(lecture_name="module_a_lecture_1")
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, response.data)

        # class size is 6; submit 3 pings to cross all thresholds
        initial_time = timezone.now()
        Ping.objects.create(
            ping_date=initial_time, lecture=lecture, student=self.student_a
        )
        Ping.objects.create(
            ping_date=initial_time, lecture=lecture, student=self.student_b
        )
        Ping.objects.create(
            ping_date=initial_time, lecture=lecture, student=self.student_c
        )

        # check new temp is equal to 3
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(3, response.data)

        # forward the time interval using FreezeGun
        with freeze_time() as frozen_datetime:
            frozen_datetime.tick(datetime.timedelta(minutes=3))

            # check api again
            response = self.client.get(
                "/tcapp/api/lectures/module_a_lecture_1/temperature/"
            )
            self.assertEqual(0, response.data)

    # test that temperature decreases immediately after a reset
    def test_decreases_after_reset(self):
        # check initial threshold level
        self.client.force_authenticate(user=self.instructor_a)
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, response.data)

        # class size is 6; submit 1 ping to cross first threshold
        Ping.objects.create(
            ping_date=timezone.now(),
            lecture=Lecture.objects.get(lecture_name="module_a_lecture_1"),
            student=User.objects.get(username="student_a"),
        )

        # check new temp is equal to 1
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(1, response.data)

        # submit reset
        Reset.objects.create(
            reset_time=timezone.now(),
            instructor=User.objects.get(username="instructor_a"),
            lecture=Lecture.objects.get(lecture_name="module_a_lecture_1"),
        )

        # check that temperature is reset back to 0
        response = self.client.get(
            "/tcapp/api/lectures/module_a_lecture_1/temperature/"
        )
        self.assertEqual(0, response.data)
