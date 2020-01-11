from rest_framework import viewsets, mixins, response,permissions
from sqlweb.baseviews import BaseView
from django.contrib.auth.models import Group,User
from rest_framework.response import Response

from .serializers import UserSerializer
from .filters import UserFilter
class UserViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定用户信息
    list:
        返回用户列表
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    filter_fields = ("username",)
    extra_perm_map = {
        "GET": ['auth.view_user']
    }


class DashboardStatusViewset(viewsets.ViewSet):
    """
    list:
    获取dashboard状态数据
    """
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        data = self.get_content_data()
        return response.Response(data)

    def get_content_data(self):
        return {
            "aa": 11,
            "bb": 22
        }

class UserInfoViewset(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        print(request)
        data = {
            "username": "admin",
            "name": "rock"
        }
        return response.Response(data)
class User_in_GroupViewset(BaseView):
    def create(self, request, *args, **kwargs):
        users_in_group={}
        request_datas=[]
        request_data = request.data
        user_id = request_data.get('id')
        user_name = User.objects.get(pk=user_id)
        count = user_name.groups.all().count()
        i=0
        while(True):
            if i == count:
                break;
            users_in_group = dict()
            groups = user_name.groups.all()[i]
            users_in_group['groups_name']=groups.name
            request_datas.append(users_in_group)
            i=i+1
        return Response(request_datas)
class user_add_groupViewset(BaseView):
    def create(self, request, *args, **kwargs):
        try:
            request_data = request.data
            print(request_data)
            user_id_temp=request_data.get('user_data')
            user_id = user_id_temp.get('id')
            user_name = User.objects.get(pk=user_id)
            group_name=request_data.get('group_name')
            group_object=Group.objects.get(name=group_name)
            Response_date=group_object.user_set.add(user_name)

            return Response('true')
        except:
            return Response('false')