# Generated by Django 2.2.10 on 2020-04-13 20:21
from polaris.models import utc_now
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polaris", "0009_transaction_paging_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="started_at",
            field=models.DateTimeField(default=utc_now),
        ),
    ]
