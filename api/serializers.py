from rest_framework import serializers

from workexperience.dynamomodels import WorkExperience
from funlinks.dynamomodels import FunLink
from interests.dynamomodels import Interests


class LucasAuthenticationSerializer(serializers.Serializer):
    auth_token = serializers.CharField(write_only=True)


class WorkExperienceSerializer(LucasAuthenticationSerializer):
    id = serializers.IntegerField(read_only=True)
    chrono_order = serializers.IntegerField()
    title = serializers.CharField()
    company = serializers.CharField()
    dates = serializers.CharField()
    location = serializers.CharField()
    body = serializers.CharField()
    img_url = serializers.CharField()
    rich_img_url = serializers.CharField()

    def create(self, validated_data):
        prior_work = WorkExperience()
        prior_work.bind(**validated_data)
        prior_work.save()
        return prior_work

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance


class FunLinkSerializer(LucasAuthenticationSerializer):
    id = serializers.IntegerField(read_only=True)
    link = serializers.CharField()
    title = serializers.CharField()

    def create(self, validated_data):
        fun_link = FunLink()
        fun_link.bind(**validated_data)
        fun_link.save()
        return fun_link

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance


class InterestsSerializer(LucasAuthenticationSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    url = serializers.CharField()

    def create(self, validated_data):
        interest = Interests()
        interest.bind(**validated_data)
        interest.save()
        return interest

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance

