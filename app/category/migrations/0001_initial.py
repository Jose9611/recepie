# Generated by Django 3.2.25 on 2025-01-03 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('level', models.IntegerField(default=1)),
                ('icon', models.TextField(blank=True, null=True)),
                ('name', models.TextField()),
                ('is_private', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('icon_url', models.TextField(blank=True, null=True)),
                ('is_visible', models.BooleanField(default=False)),
                ('priority', models.IntegerField(default=0)),
                ('disclaimer', models.TextField(default='')),
                ('added_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_user', to=settings.AUTH_USER_MODEL)),
                ('created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_created_user', to=settings.AUTH_USER_MODEL)),
                ('main_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SubCategories', to='category.category')),
                ('updated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_updated_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
    ]
