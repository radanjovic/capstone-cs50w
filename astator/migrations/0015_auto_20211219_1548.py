# Generated by Django 3.2.9 on 2021-12-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astator', '0014_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='category',
            field=models.CharField(choices=[('Adventure', 'Adventure'), ('Comedy', 'Comedy'), ('Epic', 'Epic'), ('Erotica', 'Erotica'), ('FairyTale', 'Fairy Tale'), ('Fantasy', 'Fantasy'), ('HistoricalFiction', 'Historical Fiction'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Romance', 'Romance'), ('Satire', 'Satire'), ('ScienceFiction', 'Science Fiction'), ('Thriller', 'Thriller')], max_length=25),
        ),
        migrations.AlterField(
            model_name='script',
            name='script_type',
            field=models.CharField(choices=[('Concept', 'Concept'), ('Draft', 'Draft'), ('ShortStory', 'Short Story')], max_length=20),
        ),
    ]