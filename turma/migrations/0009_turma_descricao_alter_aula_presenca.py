# Generated by Django 5.2.3 on 2025-06-20 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turma', '0008_alter_atividade_descricao_alter_aula_descricao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='turma',
            name='descricao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aula',
            name='presenca',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
