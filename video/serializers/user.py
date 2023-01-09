from rest_framework import serializers
from user.models import User,UserProfile
from coutoEditor.global_variable import BASE_URL

class UserSerializer(serializers.ModelSerializer):

    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self,obj):
        profile = UserProfile.objects.get(user=obj)
        try:
            url = f'{BASE_URL[:-1]}{profile.profile_image.url}'
        except:
            url = ""
        return url

    class Meta:
        model = User
        fields = ('id', 'username','first_name','last_name','profile_image',)



