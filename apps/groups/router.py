from rest_framework.routers import DefaultRouter
from .views import GroupsViewset,Groups_have_usersViewset,Groups_remove_usersViewset,permissionsViewset

group_router = DefaultRouter()
group_router.register('Groups', GroupsViewset, base_name="Groups")
group_router.register('Groups_have_users', Groups_have_usersViewset, base_name="Groups_have_users")
group_router.register('Groups_remove_users', Groups_remove_usersViewset, base_name="Groups_remove_users")
group_router.register('permissions', permissionsViewset, base_name="permissions")


