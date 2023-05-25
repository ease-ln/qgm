from django.conf.urls import url
from django.urls import path, include
from .views import *
from rest_framework import permissions
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Metrics recommender service API',
        default_version='v1',
        description="This is the API to work with goals, questions and metrics",
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

router = routers.DefaultRouter()
router.register('register', UserViewSet)

urlpatterns = [
    # Swagger
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Authorization
    url('', include(router.urls)),  # register
    url(r'^auth/', CustomObtainAuthToken.as_view()),  # log in
    # Goals
    url(r'^user/goals/$', UserGoalsListAPIView.as_view()),  # get user goals
    url(r'^goals/$', GoalListCreateAPIView.as_view()),  # create goal
    url(r'^goals/(?P<pk>[0-9]+)$', GoalDetailAPIView.as_view()),  # delete goal, get goal
    # Questions
    url(r'^questions/$', QuestionListCreateAPIView.as_view()),  # create question
    url(r'^questions/(?P<pk>[0-9]+)$', QuestionDetailAPIView.as_view()),  # delete question, get question
    url(r'^goal/questions/(?P<goal_id>[0-9]+)$', GoalQuestionsListAPIView.as_view()),  # get questions for goal
    # Metrics
    url(r'^metrics/$', MetricsListCreateAPIView.as_view()),
    # url(r'^metrics/(?P<pk>[0-9]+)$', MetricsDetailAPIView.as_view()),  # get metrics for question
    url(r'^question/generate-metrics/(?P<question_id>[0-9]+)$', QuestionMetricsGenerateAPIView.as_view()),  # generate metrics
    url(r'^question/assign-metrics/(?P<question_id>[0-9]+)$', QuestionMetricsAssignAPIView.as_view()),  # precooked metrics
    url(r'^question/save-metrics/(?P<question_id>[0-9]+)$', QuestionMetricsSaveAPIView.as_view()),  # metrics chosen by hand
    # url(r'^question/text-metrics/(?P<question_id>[0-9]+)$', QuestionGetAPIView.as_view()),
    # url(r'^users/goals/(?P<user_id>[0-9]+)$', UserGoalsListAPIView.as_view()),
]
