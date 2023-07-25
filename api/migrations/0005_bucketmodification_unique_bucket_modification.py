# Generated by Django 4.2.2 on 2023-06-23 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_bucketmodification_quantity'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='bucketmodification',
            constraint=models.UniqueConstraint(fields=('bucket', 'modification'), name='unique_bucket_modification'),
        ),
    ]