# Generated by Django 4.0.1 on 2022-02-10 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='projector',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('note', models.TextField(null=True)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.room')),
            ],
            options={
                'unique_together': {('room_id', 'date')},
            },
        ),
    ]