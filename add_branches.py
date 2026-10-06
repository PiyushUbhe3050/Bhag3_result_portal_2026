import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from results.models import BranchGroup

branches = [
    "स्वामी सूबोधानंद शाखा",
    "राजर्षी शाहू महाराज शाखा",
    "स्वामी ब्रम्हानंद शाखा",
    "नरवीर तानाजी मालुसरे शाखा"
]

for b_name in branches:
    branch, created = BranchGroup.objects.get_or_create(name=b_name)
    if created:
        print(f"Added: {b_name}")
    else:
        print(f"Already exists: {b_name}")
