from rest_framework.viewsets import ModelViewSet

from workexperience.dynamomodels import WorkExperience
from .serializers import WorkExperienceSerializer


class WorkExperienceViewSet(ModelViewSet):
    queryset = WorkExperience.all()
    serializer_class = WorkExperienceSerializer

