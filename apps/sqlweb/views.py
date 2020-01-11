from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Dbconf,DB_change
from .serilaizers import check_sql_serializers,db_change_serializers
from .baseviews import BaseView
from utils.check_sql import check_mysql_sql
from rest_framework import filters


class dbviewset(BaseView):
    queryset = Dbconf.objects.all()
    serializer_class = check_sql_serializers
    search_fields = ['name', 'user', 'password', 'host', 'port', 'env']
class chek_sqlViewset(BaseView):
    def create(self,request,*args,**kwargs):
        request_data = request.data
        sql_data = request_data.get('sql_content')
        user = request_data.get('user')
        password = request_data.get('password')
        host = request_data.get('host')
        post = request_data.get('port')
        sql_return = check_mysql_sql(user,password,host,post,sql_data)
        return Response(sql_return)

class db_change_Viewset(viewsets.ModelViewSet):
    queryset = DB_change.objects.all()
    serializer_class = db_change_serializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['db_user','host','port','remark']




