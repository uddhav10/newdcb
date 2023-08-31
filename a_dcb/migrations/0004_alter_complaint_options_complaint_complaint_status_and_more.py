# Generated by Django 4.2.1 on 2023-06-14 08:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('a_dcb', '0003_delete_data_complaint_created_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='complaint',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='complaint',
            name='complaint_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('rejected', 'Rejected')], default='pending', max_length=50),
        ),
        migrations.AddField(
            model_name='complaint',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]