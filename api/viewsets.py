from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog import BlogPost
from funlinks.dynamomodels import FunLink
from workexperience.dynamomodels import WorkExperience
from interests.dynamomodels import Interests

from .serializers import WorkExperienceSerializer, FunLinkSerializer, InterestsSerializer, BlogPostSerializer


class WorkExperienceViewSet(ModelViewSet):
    queryset = WorkExperience.all()
    serializer_class = WorkExperienceSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FunLinkViewSet(ModelViewSet):
    serializer_class = FunLinkSerializer
    lookup_field = 'id'

    def get_queryset(self):
        links = FunLink.all()
        return sorted(links, key=lambda link: -link.id)

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
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogPostsViewSet(ModelViewSet):
    queryset = BlogPost.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
