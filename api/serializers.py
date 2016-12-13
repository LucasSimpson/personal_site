from rest_framework import serializers

from workexperience.dynamomodels import WorkExperience


class LucasAuthenticationSerializer(serializers.Serializer):
    auth_token = serializers.CharField(write_only=True)


class WorkExperienceSerializer(LucasAuthenticationSerializer):
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
        prior_work.save()
        return prior_work
