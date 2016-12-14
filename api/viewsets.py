from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from workexperience.dynamomodels import WorkExperience
from .serializers import WorkExperienceSerializer


class WorkExperienceViewSet(ModelViewSet):
    queryset = WorkExperience.all()
    serializer_class = WorkExperienceSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
