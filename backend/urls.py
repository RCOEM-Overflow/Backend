from django.contrib import admin
from django.urls import path

from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views
# from myapp import views as myapp_views

schema_view = get_schema_view(
	openapi.Info(
		title="RCOEM OVERFLOW",
		default_version='v1',
		description="Welcome to the world of coding",
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


	path('register',views.register),
	path('login',views.login),
	path('register_contributor',views.register_contributor),
	path('update_password',views.update_password),

	path('all_contributors',views.all_contributors),
	path('all_users',views.all_users),

	path('top5_contributors',views.top5_contributors),
	path('total_users_count',views.total_users_count),
	path('total_questions_count',views.total_questions_count),
	path('total_views_count',views.total_views_count),

    path('view_all_questions',views.view_all_questions),
    path('view_search_questions',views.view_search_questions),
    path('view_trending_questions',views.view_trending_questions),
    path('view_unanswered_questions',views.view_unanswered_questions),
	path('view_specific_question',views.view_specific_question),

	path('add_question',views.add_question),
	path('add_answer',views.add_answer),

	path('upvote_question',views.upvote_question),
	path('upvote_answer',views.upvote_answer),

	path('all_tags',views.all_tags),
	path('specific_tag',views.specific_tag),


]
