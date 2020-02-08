# Generated by Django 2.2.5 on 2020-02-08 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0005_auto_20200202_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('tag_name', models.TextField(default='')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
