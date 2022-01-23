# Generated by Django 3.2.9 on 2021-12-13 14:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('astator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('script_type', models.CharField(choices=[('Concept', 'Concept'), ('Draft', 'Draft'), ('Short Story', 'Short Story')], max_length=20)),
                ('category', models.CharField(choices=[('Adventure', 'Adventure'), ('Erotica', 'Erotica'), ('Fairy Tale', 'Fairy Tale'), ('Fantasy', 'Fantasy'), ('Historical Fiction', 'Historical Fiction'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Romance', 'Romance'), ('Science Fiction', 'Science Fiction'), ('Thriller', 'Thriller')], max_length=25)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('upload', models.FileField(upload_to='scripts/%Y/%m/%D/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'rtf', 'txt'])], verbose_name='Select your script')),
                ('cover', models.ImageField(blank=True, upload_to='covers/%Y/%m/%D/', verbose_name='Select your cover image(optional)')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='amazon',
            field=models.URLField(blank=True, max_length=300, verbose_name="Amazon Author's Page URL(optional)"),
        ),
        migrations.AddField(
            model_name='user',
            name='facebook',
            field=models.URLField(blank=True, max_length=300, verbose_name='Facebook URL(optional)'),
        ),
        migrations.AddField(
            model_name='user',
            name='instagram',
            field=models.URLField(blank=True, max_length=300, verbose_name='Instagram URL(optional)'),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%D/'),
        ),
        migrations.AddField(
            model_name='user',
            name='twitter',
            field=models.URLField(blank=True, max_length=300, verbose_name='Twitter URL(optional)'),
        ),
        migrations.AddField(
            model_name='user',
            name='youtube',
            field=models.URLField(blank=True, max_length=300, verbose_name='YouTube URL(optional)'),
        ),
        migrations.CreateModel(
            name='Sugestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestion', models.TextField(verbose_name='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggestion', to='astator.script')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggestion', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='script',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='script', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ReadLater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_later', to='astator.script')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_later', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storyline_rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('characters_rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('writing_rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='astator.script')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_authors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='astator.script')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
