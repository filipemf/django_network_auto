# Generated by Django 5.1 on 2024-08-15 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=255)),
                ('ip_address', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('ssh_port', models.IntegerField(default=22)),
                ('vendor', models.CharField(choices=[('cisco', 'Cisco'), ('arista', 'Arista'), ('juniper', 'Juniper')], max_length=255)),
            ],
        ),
    ]
