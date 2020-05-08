from account.models import CstdUser, CstdUserRole, CstdRole
from rest_framework import serializers


class CstdUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CstdUser
        fields = ['id', 'username', 'email', 'phone']


class CstdUserRoleInfoSerializer(serializers.models):
    # roles = serializers.SerializerMethodField('get_role_names')

    class Meta:
        model = CstdUser
        fields = ['id', 'username', 'email', 'phone', 'roles']

    # def get_role_names(self, obj):
    #         try:
    #             usr_id = obj.devices.filter(pl_belong=self.context['user_id'])
    #             cstd_user_roles = CstdUserRole.objects.filter(usr_id)
    #             cstd_user_role_list = []
    #             for cstd_user_role in cstd_user_roles:
    #                 role = CstdRole.objects.get(pk=cstd_user_role.role)
    #                 cstd_user_role_list.append(role.name)
    #             # if pl_ds_queryset.exists():
    #             #     print(pl_ds_queryset)
    #             #     serializer = DeviceSerializer(instance=pl_ds_queryset, context=self.context, many=True)
    #                 return cstd_user_role_list
    #             else:
    #                 # print(pl_ds_queryset)
    #                 return []
    #         except Exception as e:
    #             print(e)
    #             return []
