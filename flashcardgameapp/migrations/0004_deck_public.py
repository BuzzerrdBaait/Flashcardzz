# Generated by Django 4.2.4 on 2023-11-15 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcardgameapp', '0003_rename_page_text_card_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
