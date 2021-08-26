from rest_framework import serializers
from aiLooker_app.models import Tbladvtbsc

class TbladvtbscSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'advtno',
            'advttpcd',
        )
        model = Tbladvtbsc