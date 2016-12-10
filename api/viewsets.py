from rest_framework.viewsets import ModelViewSet

from .dynamomodels import PriorWork
from .serializers import PriorWorkSerializer


class PriorWorkViewSet(ModelViewSet):
    queryset = PriorWork.all()
    serializer_class = PriorWorkSerializer

