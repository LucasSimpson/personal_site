from rest_framework import serializers

from workexperience.dynamomodels import WorkExperience
from funlinks.dynamomodels import FunLink

class LucasAuthenticationSerializer(serializers.Serializer):
    auth_token = serializers.CharField(write_only=True)


class WorkExperienceSerializer(LucasAuthenticationSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name='work_experience-detail', read_only=True, lookup_field='id', lookup_url_kwarg='pk')
    id = serializers.IntegerField(read_only=True)
    chrono_order = serializers.IntegerField()
    title = serializers.CharField()
    company = serializers.CharField()
    dates = serializers.CharField()
    location = serializers.CharField()
    body = serializers.CharField()
    img_url = serializers.CharField()

    def create(self, validated_data):
        prior_work = WorkExperience()
        prior_work.chrono_order = validated_data['chrono_order']
        prior_work.title = validated_data['title']
        prior_work.company = validated_data['company']
        prior_work.dates = validated_data['dates']
        prior_work.location = validated_data['location']
        prior_work.body = validated_data['body']
        prior_work.img_url = validated_data['img_url']
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
        #fun_link.link = validated_data['link']
        #fun_link.title = validated_data['title']
        fun_link.bind(**validated_data)
        fun_link.save()
        return fun_link

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance