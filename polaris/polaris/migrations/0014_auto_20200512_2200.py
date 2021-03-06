# Generated by Django 2.2.12 on 2020-05-12 22:00

from django.db import migrations
from polaris.models import EncryptedTextField


in_memory_seeds = []


def hold_seeds_in_memory(apps, schema_editor):
    """
    Hold unencrypted seeds in memory and remove them from the DB

    This is necessary because if unencrypted seeds are retrieved
    from the DB by an Asset object after the migration, it will
    fail when attempted to decrypt them.
    """
    Asset = apps.get_model("polaris", "Asset")
    for asset in Asset.objects.exclude(distribution_seed__isnull=True):
        in_memory_seeds.append((asset.id, asset.distribution_seed))
        asset.distribution_seed = None
        asset.save()


def reassign_seeds(apps, schema_editor):
    """
    Now that the Asset.distribution_seed column encrypts seeds
    before insertion we can reinsert the unencrypted seeds.
    """
    Asset = apps.get_model("polaris", "Asset")
    for (id, seed) in in_memory_seeds:
        Asset.objects.filter(id=id).update(distribution_seed=seed)


class Migration(migrations.Migration):

    dependencies = [
        ("polaris", "0013_transaction_protocol"),
    ]

    operations = [
        migrations.RunPython(hold_seeds_in_memory),
        migrations.AlterField(
            model_name="asset",
            name="distribution_seed",
            field=EncryptedTextField(null=True),
        ),
        migrations.RunPython(reassign_seeds),
    ]
