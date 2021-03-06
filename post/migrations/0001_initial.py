# Generated by Django 3.1.7 on 2021-03-23 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250, verbose_name='Kullanıcı Adı')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Başlık')),
                ('content', models.TextField(verbose_name='İçerik')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Yayın Tarihi')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Resim')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.author')),
            ],
            options={
                'ordering': ['-date', 'id'],
            },
        ),
    ]
