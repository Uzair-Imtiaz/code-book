# Generated by Django 4.2.2 on 2023-07-09 09:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='The title of the project.', max_length=200, null=True)),
                ('description', models.TextField(blank=True, help_text='The detailed description of the project.', null=True)),
                ('featured_image', models.ImageField(blank=True, help_text='The featured image(s) of the project.', null=True, upload_to='')),
                ('youtube_link', models.CharField(blank=True, help_text='The link to the YouTube video of the project.', max_length=200, null=True)),
                ('demo_link', models.CharField(blank=True, help_text='The link to the demo of the project(if deployed).', max_length=200, null=True)),
                ('source_code_link', models.CharField(blank=True, help_text='The link to the source code of the project.', max_length=200, null=True)),
                ('user', models.ForeignKey(blank=True, help_text='The user that created the project.', on_delete=django.db.models.deletion.CASCADE, related_name='project', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.CharField(blank=True, choices=[('Up', 'Up'), ('Down', 'Down')], help_text='The vote choice (Up or Down).', max_length=20)),
                ('project', models.ForeignKey(blank=True, help_text='The project being voted on.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='core.project')),
                ('user', models.ForeignKey(blank=True, help_text='The user who voted.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vote', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, help_text='The content of the review.', null=True)),
                ('project', models.ForeignKey(blank=True, help_text='The project that is being reviewed.', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.project')),
                ('user', models.ForeignKey(blank=True, help_text='The user who wrote the review.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
