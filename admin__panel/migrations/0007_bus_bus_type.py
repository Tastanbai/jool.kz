# Generated by Django 5.0.6 on 2024-09-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin__panel', '0006_seat_delete_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='bus_type',
            field=models.CharField(choices=[('sitting', 'Сидящий'), ('sleeping', 'Спящий')], default='sitting', max_length=10),
        ),
    ]
