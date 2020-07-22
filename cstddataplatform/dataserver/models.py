from django.db import models

# Create your models here.
# Create your models here.
class UserLabelData(models.Model):
    name = models.CharField('名称', max_length=50)
    creator = models.CharField('地图创建人', max_length=50)
    creator_id = models.IntegerField(verbose_name=u'地图创建人id')
    # layer = models.IntegerField('图层叠加顺序0 1 2', default=0)
    # group = models.CharField('图层组', max_length=30)
    # path = models.CharField('数据路径', max_length=255)
    # map_data_id = models.IntegerField(verbose_name=u'地图数据id', default=0)
    # map_data = models.CharField('图层组', max_length=30)
    is_deleted = models.BooleanField('已删除', default=False)
    description = models.CharField('描述', max_length=50, blank=True, default='')
    create_time = models.DateTimeField('开始时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now_add=True)
    label_data = models.BinaryField('用户标注数据,geojson的pbf版本', blank=False)

    def __str__(self):
        return self.name + self.creator

    class Meta:
        verbose_name = '用户标注地图层'
        verbose_name_plural = '用户标注地图层'
