from rest_framework import serializers

from workexperience.dynamomodels import WorkExperience


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
        # TODO have some sort of Model.bind(data) method or something
        # or set getters/setters on model attributes for typecasting?

        print('in update')
        print('%s :: %s' % (instance, validated_data))

        return instance