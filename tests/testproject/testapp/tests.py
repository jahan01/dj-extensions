from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User, Permission

from django.core.urlresolvers import reverse
from .views import *
from .models import *


class BaseTest(TestCase):
    def setUp(self, url):
        self.view_url = url
        self.request_factory = RequestFactory()

class BasePermissionTest(BaseTest):

    def setUp(self, url):
        self.user = User.objects.create_user(username='user', password='user')
        super(BasePermissionTest, self).setUp(url)

    def generate_request(self, user='anonymous'):
        request = self.request_factory.get(self.view_url)
        # if user == 'anonymous':
        #     request.user = AnonymousUser()
        # else:
        #     request.user = user
        request.user = user
        return request

class TestSinglePermissionRequired(BasePermissionTest):

    def setUp(self):
        url = reverse('permission_required')
        super(TestSinglePermissionRequired, self).setUp(url)

    def test_anonomous_user(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next={0}'.format(self.view_url))

    def test_unauthorised_user(self):
        request = self.generate_request(self.user)
        response = PermissionView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/login/?next={0}'.format(self.view_url))

    def test_authorised_user(self):
        permission = Permission.objects.get(codename='add_sample')
        self.user.user_permissions.add(permission)
        # self.client.login(username='user', password='user')
        # response = self.client.get(self.view_url)
        request = self.generate_request(self.user)
        response = PermissionView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success Get")

class TestMultiplePermissionRequired(BasePermissionTest):

    def setUp(self):
        url = reverse('multiple_permission_required')
        super(TestMultiplePermissionRequired, self).setUp(url)

    def test_anonomous_user(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next={0}'.format(self.view_url))

    def test_unauthorised_user(self):
        request = self.generate_request(self.user)
        response = MultiplePermissionView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/login/?next={0}'.format(self.view_url))

    def test_not_all_permission_user(self):
        permission = Permission.objects.get(codename='add_sample')
        self.user.user_permissions.add(permission)
        request = self.generate_request(self.user)
        response = MultiplePermissionView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/login/?next={0}'.format(self.view_url))

    def test_authorised_user(self):
        permission1 = Permission.objects.get(codename='add_sample')
        permission2 = Permission.objects.get(codename='change_sample')
        self.user.user_permissions.add(permission1)
        self.user.user_permissions.add(permission2)
        request = self.generate_request(self.user)
        response = MultiplePermissionView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success Get")

class TestAjaxOnlyMixin(BaseTest):

    def setUp(self):
        url = reverse('ajax_only')
        super(TestAjaxOnlyMixin, self).setUp(url)

    def test_non_ajax(self):
        request = self.request_factory.get(self.view_url)
        response = AjaxOnlyView.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_ajax_request(self):
        request = self.request_factory.get(self.view_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = AjaxOnlyView.as_view()(request)
        self.assertEqual(response.status_code, 200)

class TestFilterMixin(BaseTest):

    def setUp(self):
        url = reverse('filter_view')
        super(TestFilterMixin, self).setUp(url)
        for i in range(1, 11):
            record = Sample.objects.create(field1=('string1'+str(i*10)), field2 = i)
            record.save()
            record = Sample.objects.create(field1=('string2'+str(i*10)), field2 = i)
            record.save()

    def check(self, param, count):
        request_url = self.view_url + param
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ("Count " + str(count)))

    def test_single_condition(self):
        self.check('?number=1', 2)
        self.check('?string=string1', 10)

    def test_multiple_conditions(self):
        self.check('?number=1&string=string1', 1)
        self.check('?string=string2&number=2', 1)

class TestPaginationMixin(BaseTest):

    def setUp(self):
        url = reverse('paginated_view')
        super(TestPaginationMixin, self).setUp(url)
        for i in range(1, 16):
            record = Sample.objects.create(field1=('string1'+str(i*10)), field2 = i)
            record.save()

    def check(self, param, prev, next):
        request_url = self.view_url + param
        response = self.client.get(request_url)
        self.assertEqual(response.content.decode("utf-8"), "Page dict:- next:%s, prev:%s" % (next, prev))

    def check_not_found(self, param):
        request_url = self.view_url + param
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 404)

    def test(self):
        self.check('?page=1', '0:0', '1:6')
        self.check('?page=2', '0:1', '2:7')
        self.check('?page=3', '0:2', '3:8')
        self.check('?page=15', '9:14', '15:20')

    def test_not_found(self):
        self.check_not_found('?page=0')
        self.check_not_found('?page=16')
