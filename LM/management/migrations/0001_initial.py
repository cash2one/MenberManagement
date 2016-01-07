# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('price', models.FloatField()),
                ('author', models.CharField(max_length=128)),
                ('pubDate', models.DateField()),
                ('typ', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('course_name', models.CharField(verbose_name='课程名', max_length=50)),
                ('course_subject', models.TextField(verbose_name='课程纲要')),
                ('beizhu', models.TextField(verbose_name='备注')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
            },
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('desc', models.TextField()),
                ('img', models.ImageField(upload_to='image')),
                ('book', models.ForeignKey(to='management.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Menbers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('menber_name', models.CharField(verbose_name='姓名', max_length=30)),
                ('menber_address', models.CharField(verbose_name='地址', max_length=60)),
                ('menber_city', models.CharField(verbose_name='城市', max_length=50)),
                ('menber_tel', models.CharField(verbose_name='电话', max_length=50)),
                ('course', models.ManyToManyField(to='management.Courses')),
            ],
            options={
                'verbose_name': '学员',
                'verbose_name_plural': '学员',
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nickname', models.CharField(max_length=16)),
                ('permission', models.IntegerField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('store_name', models.CharField(verbose_name='店名', max_length=50)),
                ('store_brand', models.CharField(verbose_name='品牌', max_length=50)),
                ('store_size', models.CharField(verbose_name='规模', max_length=30)),
                ('store_address', models.CharField(verbose_name='地址', max_length=60)),
                ('stroe_city', models.CharField(verbose_name='城市', max_length=30)),
                ('store_boss', models.CharField(verbose_name='老板', max_length=30)),
                ('store_tel', models.CharField(verbose_name='电话', max_length=30)),
            ],
            options={
                'verbose_name': '店铺',
                'verbose_name_plural': '店铺',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('teacher_name', models.CharField(verbose_name='姓名', max_length=30)),
                ('teacher_sex', models.CharField(verbose_name='性别', max_length=10)),
                ('teacher_organize', models.CharField(verbose_name='机构', max_length=50)),
                ('teacher_address', models.CharField(verbose_name='地址', max_length=60)),
                ('teacher_contact', models.CharField(verbose_name='联系人', max_length=30)),
                ('teacher_tel', models.CharField(verbose_name='联系电话', max_length=50)),
                ('beizhu', models.TextField(verbose_name='备注')),
            ],
            options={
                'verbose_name': '讲师',
                'verbose_name_plural': '讲师',
            },
        ),
        migrations.AddField(
            model_name='menbers',
            name='menber_store',
            field=models.ForeignKey(verbose_name='店名', to='management.Stores'),
        ),
        migrations.AddField(
            model_name='courses',
            name='teacher',
            field=models.ManyToManyField(to='management.Teacher'),
        ),
    ]
