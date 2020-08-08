# Generated by Django 3.1 on 2020-08-08 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rest', '0004_auto_20200807_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='confession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.confession'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vote',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_votes', to='rest.comment'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='confession',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='confession_votes', to='rest.confession'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote_type',
            field=models.IntegerField(choices=[(1, 'UPVOTE'), (-1, 'DOWNVOTE')], default=1),
        ),
    ]
