from rest_framework import serializers
from .models import Dbconf,DB_change

class check_sql_serializers(serializers.ModelSerializer):

    class Meta:
        model = Dbconf
        fields = "__all__"



class db_change_serializers(serializers.ModelSerializer):
    class Meta:
        model = DB_change
        fields = "__all__"
