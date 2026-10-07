from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from .models import TodoItem
from .views import index


class DashboardTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='dashboard-user',
			password='test-password',
		)
		self.factory = RequestFactory()

	def test_dashboard_counts_items_in_one_query(self):
		TodoItem.objects.create(
			user=self.user,
			title='Completed task',
			description='',
			date_due='2026-10-08T12:00:00Z',
			is_completed=True,
		)
		TodoItem.objects.create(
			user=self.user,
			title='Pending task',
			description='',
			date_due='2026-10-09T12:00:00Z',
		)

		request = self.factory.get('/')
		request.user = self.user
		with patch('todo.views.render', return_value=HttpResponse()) as render:
			with self.assertNumQueries(1):
				response = index(request)

		self.assertEqual(response.status_code, 200)
		context = render.call_args.args[2]
		self.assertEqual(context['total_todos'], 2)
		self.assertEqual(context['completed_todos'], 1)
		self.assertEqual(context['pending_todos'], 1)
