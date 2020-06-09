from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
import django.utils.timezone as timezone
from django.db.backends.sqlite3.base import DatabaseFeatures # 关键设置
DatabaseFeatures.supports_microsecond_precision = False # 关键设置

from tileserver.models import MapData


class CstdUserManager(BaseUserManager):

    @classmethod
    def normalize_phone(cls, phone):
        """
        Normalize the phonenum.
        """
        import re
        # 验证手机号是否正确
        phone = phone or ''
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        res = re.search(phone_pat, phone)
        if res:
            return phone
        else:
            return ValueError

    def create_user(self, phone, email, username, password=None):
        if not phone:
            raise ValueError('Users must have an phone number')
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(username=username, phone=self.normalize_phone(phone), email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, username, password=None):
        user = self.create_user(username=username, password=password, phone=self.normalize_phone(phone),
                                email=self.normalize_email(email))
        user.is_admin = True
        user.is_authenticated = True
        user.save(using=self._db)
        return user


class CstdUser(AbstractBaseUser):
    """
    地图用户
    """
    username = models.CharField('username', max_length=50, unique=True)
    alias = models.CharField('姓名', max_length=50, default='')
    email = models.EmailField('email', max_length=255)
    phone = models.CharField('phone', max_length=13, default='')
    is_active = models.BooleanField('已激活', default=False)
    is_admin = models.BooleanField('超级管理员', default=False)
    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    objects = CstdUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_alias_name(self):
        return self.alias

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    # @property
    # def is_staff(self):
    #     return self.is_admin

    # @property
    # def is_admin(self):
    #     return self.is_admin
    # @property
    # def dept_name(self):
    #     dept_id = self.dept_id
    #     dept_object = LoonDept.objects.filter(id=dept_id)
    #     if dept_object:
    #         return dept_object[0].name
    #     else:
    #         return '部门id不存在'

    def get_dict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        dict_result = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            elif attr == 'password':
                pass
            elif attr == 'creator':
                creator_obj = CstdUser.objects.filter(username=getattr(self, attr)).first()
                if creator_obj:
                    dict_result['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias,
                                                       creator_username=creator_obj.username)
                else:
                    dict_result['creator_info'] = dict(creator_id=0, creator_alias='', creator_username=getattr(self, attr))
            else:
                dict_result[attr] = getattr(self, attr)

        return dict_result

    def get_json(self):
        import json
        dict_result = self.get_dict()
        return json.dumps(dict_result)
    #
    # EMAIL_FIELD = 'email'
    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']
    #
    # class Meta:
    #     verbose_name = _('user')
    #     verbose_name_plural = _('users')
    #     abstract = True

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'user'


class CstdRole(models.Model):
    name = models.CharField(verbose_name=u'角色名称', max_length=100)
    description = models.CharField(verbose_name=u'角色描述', max_length=200, blank=True, null=True)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)
    modified = models.DateTimeField(u'更新时间', auto_now=True)
    deleted = models.BooleanField(u'己删除', default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'


class CstdUserRole(models.Model):
    user = models.IntegerField(verbose_name=u'用户')
    role = models.IntegerField(verbose_name=u'角色')
    created = models.DateTimeField(u'创建时间', auto_now_add=True)
    modified = models.DateTimeField(u'更新时间', auto_now=True)
    deleted = models.BooleanField(u'己删除', default=False)

    def __str__(self):
        return '{}-{}'.format(self.user, self.role)


class MapUser(models.Model):
    start_time = models.DateTimeField('开始时间', auto_now_add=True)
    end_time = models.DateTimeField('结束时间', auto_now_add=True)
    # maps = models.ManyToManyField(Map, related_name='mapid')
    # users = models.ManyToManyField(CstdUser, related_name='userid')
    user_id = models.IntegerField(verbose_name=u'用户')
    map_id = models.IntegerField(verbose_name=u'地图')

    class Meta:
        verbose_name = '用户地图'
        verbose_name_plural = '用户地图'
    # def __str__(self):
    #     return self.name


class MapDataUser(models.Model):
    start_time = models.DateTimeField('开始时间', auto_now_add=True)
    end_time = models.DateTimeField('结束时间', auto_now_add=True)
    # maps = models.ManyToManyField(Map, related_name='mapid')
    # users = models.ManyToManyField(CstdUser, related_name='userid')
    user_id = models.IntegerField(verbose_name=u'数据使用用户')
    map_data_id = models.IntegerField(verbose_name=u'地图数据')
    creator_id = models.IntegerField(verbose_name=u'数据创建用户')
    # user = models.ForeignKey(MapUser, related_name='MapUser', on_delete=models.CASCADE)
    # map_data = models.ForeignKey(MapData, related_name='MapUser', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '用户地图数据'
        verbose_name_plural = '用户地图数据'
    # def __str__(self):
    #     return self.name
