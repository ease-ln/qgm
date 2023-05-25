import json

from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import *
from django.contrib.auth.models import User
from .serializers import *

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .metrics_generator import create_metrics


# Authorization Endpoints
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Goals Endpoints
class UserGoalsListAPIView(generics.ListAPIView):
    """
    get:
    API endpoint that returns a list of goals assigned to the current user.
    """
    serializer_class = GoalSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Goal.objects.filter(user_id=self.request.user.id)


class GoalDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    API endpoint that returns the goal with this primary key.
    put:
    API endpoint that updates the goal with this primary key.
    patch:
    API endpoint that partially updates the goal with this primary key.
    delete:
    API endpoint that deletes the goal with this primary key.
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class GoalListCreateAPIView(generics.ListCreateAPIView):
    """
    get:
    API endpoint that returns a list of all existing goals.
    post:
    API endpoint to create a new goal.
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


# Questions Endpoints
class GoalQuestionsListAPIView(generics.ListAPIView):
    """
    get:
    API endpoint that returns a list of questions assigned to the goal.
    """
    serializer_class = QuestionSerializer
    lookup_field = "goal_id"

    def get_queryset(self):
        return Question.objects.filter(goal_id=self.kwargs['goal_id'])


class QuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    API endpoint that returns the question with this primary key.
    put:
    API endpoint that updates the question with this primary key.
    patch:
    API endpoint that partially updates the question with this primary key.
    delete:
    API endpoint that deletes the question with this primary key.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionListCreateAPIView(generics.ListCreateAPIView):
    """
    get:
    API endpoint that returns a list of all existing questions.
    post:
    API endpoint to create a new question.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# Metrics Endpoints
class MetricsListCreateAPIView(generics.ListCreateAPIView):
    """
    get:
    API endpoint that returns a list of all existing metrics.
    post:
    API endpoint that creates a new metrics.
    """
    queryset = Metrics.objects.all()
    serializer_class = MetricsSerializer


class MetricsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    API endpoint that returns the metrics with this primary key.
    put:
    API endpoint that updates the metrics with this primary key.
    patch:
    API endpoint that partially updates the metrics with this primary key.
    delete:
    API endpoint that deletes the metrics with this primary key.
    """
    queryset = Metrics.objects.all()
    serializer_class = MetricsSerializer


class QuestionGetAPIView(APIView):

    def get(self, request, question_id):
        """API endpoint to get question with string metrics values"""
        question = Question.objects.filter(id=question_id)
        content = question.values()[0].get('content')
        goal_id = question.values()[0].get('goal_id_id')
        goal = Goal.objects.get(id=goal_id)
        question = Question.objects.get(id=question_id)
        metrics_ids = question.metrics.all()
        metrics_names = []
        for metric_id in metrics_ids:
            metrics_names.append(str(metric_id))
        data = {'content': content, 'goal_id_id': goal_id}
        ser = Question(content=content, goal_id_id=goal_id)
        ser.save()
        ser.metrics.set([metrics_names])
        return Response(ser, status=status.HTTP_201_CREATED)


class QuestionMetricsGenerateAPIView(APIView):

    def patch(self, request, question_id):
        """API endpoint to generate metrics and assign them to the question"""
        question = Question.objects.filter(id=question_id)
        content = question.values()[0].get('content')
        metrics = create_metrics(content, question_id)
        data = {'metrics': metrics}
        serializer = QuestionSerializer(question.first(), data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionMetricsAssignAPIView(APIView):

    def patch(self, request, question_id):
        """API endpoint to generate metrics and assign them to the question"""
        question = Question.objects.filter(id=question_id)
        content = question.values()[0].get('content')
        data = {'metrics': ['Time', 'Number of people', 'Money']}
        serializer = QuestionSerializer(question.first(), data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionMetricsSaveAPIView(APIView):

    def patch(self, request, question_id):
        """API endpoint to generate metrics and assign them to the question"""
        question = Question.objects.filter(id=question_id)
        body_unicode = request.body.decode('utf-8')
        metrics = json.loads(body_unicode)
        newList = []
        for item in metrics:
            newList.append(item["name"])
        data = {'metrics': newList}
        serializer = QuestionSerializer(question.first(), data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
