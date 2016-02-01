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
            name='Courses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('course_name', models.CharField(max_length=50, verbose_name='课程名')),
                ('course_subject', models.TextField(verbose_name='课程纲要')),
                ('teacher', models.TextField(verbose_name='老师')),
                ('organize', models.CharField(max_length=50, verbose_name='培训机构')),
                ('course_date', models.DateField(verbose_name='培训日期')),
                ('course_address', models.CharField(max_length=50, verbose_name='授课场地')),
                ('beizhu', models.TextField(verbose_name='备注')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
            },
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('f_tel', models.CharField(max_length=30, verbose_name='朋友电话')),
                ('f_name', models.CharField(max_length=30, verbose_name='朋友姓名')),
                ('f_gift', models.CharField(max_length=30, verbose_name='朋友礼品')),
                ('f_date', models.DateField(verbose_name='送礼日期')),
                ('f_remarks', models.TextField(verbose_name='备注', blank=True)),
            ],
            options={
                'verbose_name': '朋友',
                'verbose_name_plural': '朋友',
            },
        ),
        migrations.CreateModel(
            name='Menbers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('permission', models.IntegerField()),
                ('menber_name', models.CharField(max_length=30, verbose_name='姓名')),
                ('menber_address', models.CharField(max_length=60, verbose_name='地址')),
                ('menber_city', models.CharField(max_length=50, verbose_name='城市')),
                ('menber_tel', models.CharField(max_length=50, verbose_name='电话')),
                ('menber_store', models.CharField(max_length=50, verbose_name='店名')),
                ('menber_brand', models.CharField(max_length=50, verbose_name='品牌')),
                ('menber_typ', models.CharField(max_length=60, verbose_name='级别')),
            ],
            options={
                'verbose_name': '学员',
                'verbose_name_plural': '学员',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('tel', models.CharField(max_length=30, verbose_name='电话')),
                ('name', models.CharField(max_length=30, verbose_name='姓名')),
                ('gift', models.CharField(max_length=30, verbose_name='礼品')),
                ('pdate', models.DateField(auto_now_add=True, verbose_name='领取日期')),
                ('remarks', models.TextField(verbose_name='备注', blank=True)),
            ],
            options={
                'verbose_name': '发起人',
                'ordering': ['-pdate'],
                'verbose_name_plural': '发起人',
            },
        ),
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('sign_mood', models.CharField(max_length=50, verbose_name='一句话')),
                ('sign_date', models.DateTimeField(auto_now_add=True, verbose_name='签到时间')),
                ('courses', models.ForeignKey(to='management.Courses')),
            ],
            options={
                'verbose_name': '签到',
                'ordering': ['-sign_date'],
                'verbose_name_plural': '签到',
            },
        ),
        migrations.AddField(
            model_name='menbers',
            name='sign',
            field=models.ManyToManyField(to='management.Sign'),
        ),
        migrations.AddField(
            model_name='menbers',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friends',
            name='person',
            field=models.ForeignKey(to='management.Person'),
        ),
    ]
