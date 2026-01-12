from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "recommender"

urlpatterns = [
    path("", views.start_questionnaire, name="start"),
    path("q/", views.question, name="question"),
    path("result/<int:event_id>/", views.result, name="result"),
    path("analytics/", views.analytics, name="analytics"),
    path("analytics/<int:event_id>/", views.analytics_detail, name="analytics_detail"),
    path("restart/", views.restart, name="restart"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
