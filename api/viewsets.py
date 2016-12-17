from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from funlinks.dynamomodels import FunLink
from workexperience.dynamomodels import WorkExperience
from interests.dynamomodels import Interests

from .serializers import WorkExperienceSerializer, FunLinkSerializer, InterestsSerializer


class WorkExperienceViewSet(ModelViewSet):
    queryset = WorkExperience.all()
    serializer_class = WorkExperienceSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FunLinkViewSet(ModelViewSet):
    queryset = FunLink.all()
    serializer_class = FunLinkSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class InterestsViewSet(ModelViewSet):
    queryset = Interests.all()
    serializer_class = InterestsSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serialzer = self.get_serializer(instance)
        return Response(serialzer.data)
