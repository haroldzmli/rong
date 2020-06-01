from django.db import models


# Create your models here.
class Map(models.Model):
    name = models.CharField('名称', max_length=50)
    creator = models.CharField('地图创建人', max_length=50)
    creator_id = models.IntegerField(verbose_name=u'地图创建人id')
    # layer = models.IntegerField('图层叠加顺序0 1 2', default=0)
    # group = models.CharField('图层组', max_length=30)
    # path = models.CharField('数据路径', max_length=255)
    # map_data_id = models.IntegerField(verbose_name=u'地图数据id', default=0)
    map_data = models.CharField('图层组', max_length=30)
    is_deleted = models.BooleanField('已删除', default=False)
    description = models.CharField('描述', max_length=50, blank=True, default='')
    create_time = models.DateTimeField('开始时间', auto_now_add=True)
    modified_time = models.DateTimeField('结束时间', auto_now_add=True)

    def __str__(self):
        return self.group + self.layer

    class Meta:
        verbose_name = '地图'
        verbose_name_plural = '地图'


class MapData(models.Model):
    name = models.CharField('名称', max_length=50, default='')
    author = models.CharField('数据创建人', max_length=50)
    author_id = models.IntegerField(verbose_name=u'数据创建人id')
    description = models.CharField('描述', max_length=50, default='', null=True, blank=True)
    is_deleted = models.BooleanField('已删除', default=False)
    create_time = models.DateTimeField('开始时间', auto_now_add=True)
    end_time = models.DateTimeField('结束时间', auto_now_add=True)
    save_path = models.CharField('数据路径', max_length=255, default='')
    save_name = models.CharField('数据保存名称', max_length=255, default='')
    # file = models.FileField(null=False)

    def __str__(self):
        return self.name + self.author

    class Meta:
        verbose_name = '用户地图数据'
        verbose_name_plural = '用户地图数据'
