# Generated by Django 3.1.2 on 2020-10-13 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20201013_0538'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='posttab',
            unique_together={('id', 'article_id')},
        ),
    ]