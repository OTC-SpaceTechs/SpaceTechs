from django.db import migrations

OFFICER_GROUPS = [
    "Chair",
    "Vice-Chair",
    "Secretary",
    "Treasurer",
    "Director of Projects",
    "Director of Research",
    "Director of Outreach",
    "SEDS Rep",
    "Member-at-large",
]

def create_officer_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    for name in OFFICER_GROUPS:
        Group.objects.get_or_create(name=name)

def delete_officer_groups(apps, schema_editor):
    Group = apps.get_model('auth','Group')
    Group.objects.filter(name__in=OFFICER_GROUPS).delete()

class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]
    operations = [
        migrations.RunPython(create_officer_groups, delete_officer_groups),
    ]