# Generated by Django 5.1.3 on 2024-11-27 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0011_sanphamban_phan_tram_chiet_khau_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanphamnhapkho',
            name='thanh_tien',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
