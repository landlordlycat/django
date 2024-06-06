# Generated by Django 5.0.6 on 2024-06-06 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name': '博客', 'verbose_name_plural': '博客'},
        ),
        migrations.AlterModelOptions(
            name='blogcategory',
            options={'verbose_name': '分类', 'verbose_name_plural': '分类'},
        ),
        migrations.AlterModelOptions(
            name='blogcomment',
            options={'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
        migrations.RemoveField(
            model_name='blogcategory',
            name='description',
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=200, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='name',
            field=models.CharField(max_length=200, verbose_name='分类名称'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='content',
            field=models.TextField(verbose_name='评论内容'),
        ),
    ]
