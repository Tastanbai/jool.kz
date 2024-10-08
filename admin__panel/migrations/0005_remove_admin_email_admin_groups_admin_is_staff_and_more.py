# Generated by Django 5.1 on 2024-08-08 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin__panel', '0004_admin'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='email',
        ),
        migrations.AddField(
            model_name='admin',
            name='groups',
            field=models.ManyToManyField(related_name='admin_groups', to='auth.group'),
        ),
        migrations.AddField(
            model_name='admin',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='admin',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='admin',
            name='user_permissions',
            field=models.ManyToManyField(related_name='admin_user_permissions', to='auth.permission'),
        ),
        migrations.AddField(
            model_name='admin',
            name='username',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
