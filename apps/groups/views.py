import json
from rest_framework import viewsets
from django.contrib.auth.models import Group,User,Permission
from .serilaizers import GroupSerializer,permissionsSerializer
from .filter import GroupFilter
from rest_framework import filters
from rest_framework.response import Response
from sqlweb.baseviews import BaseView


class GroupsViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    filter_fields = ("name",)

class Groups_have_usersViewset(BaseView):
    def create(self, request, *args, **kwargs):
        users_in_group={}
        request_datas=[]
        request_data = request.data
        group_id = request_data.get('group_id')
        group_name = Group.objects.get(pk=group_id)
        group_object = Group.objects.get(name=group_name)
        count = group_object.user_set.all().count()
        i=0
        while(True):
            if i == count:
                break;
            users_in_group = dict()
            users = group_object.user_set.all()[i]
            users_in_group['username']=users.username
            users_in_group['email']=users.email
            request_datas.append(users_in_group)
            i=i+1
        return Response(request_datas)

class Groups_have_usersViewset(BaseView):
            def create(self, request, *args, **kwargs):
                users_in_group = {}
                request_datas = []
                request_data = request.data
                group_id = request_data.get('group_id')
                group_name = Group.objects.get(pk=group_id)
                group_object = Group.objects.get(name=group_name)
                count = group_object.user_set.all().count()
                i = 0
                while (True):
                    if i == count:
                        break;
                    users_in_group = dict()
                    users = group_object.user_set.all()[i]
                    users_in_group['username'] = users.username
                    users_in_group['email'] = users.email
                    request_datas.append(users_in_group)
                    i = i + 1
                return Response(request_datas)
class Groups_remove_usersViewset(BaseView):
    def create(self, request, *args, **kwargs):
        try:
            request_data = request.data
            group_id_temp=request_data.get('group_data')
            group_id=group_id_temp.get('group_id')
            group_object = Group.objects.get(pk=group_id)
            user_name = request_data.get('user_name')
            user_object = User.objects.get(username=user_name)
            group_object.user_set.remove(user_object)
            return Response('true')
        except:
            return Response('false')

class permissionsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = permissionsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','codename']
    ordering_fields=('id')