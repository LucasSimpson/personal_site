from rest_framework import serializers

from .dynamomodels import PriorWork


class PriorWorkSerializer(serializers.Serializer):
    chrono_order = serializers.IntegerField()
    title = serializers.CharField()

    def create(self, validated_data):
        prior_work = PriorWork()
        prior_work.chrono_order = validated_data['chrono_order']
        prior_work.title = validated_data['title']
        prior_work.save()
        return prior_work
