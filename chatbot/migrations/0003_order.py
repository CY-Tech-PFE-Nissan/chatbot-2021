# Generated by Django 3.2.8 on 2021-11-24 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_auto_20211028_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.TextField()),
                ('sub_topic', models.TextField()),
                ('video_title', models.TextField()),
                ('order', models.TextField()),
                ('url_api', models.TextField()),
                ('sequence_tree', models.TextField()),
                ('topic_terms', models.TextField()),
            ],
        ),
    ]
