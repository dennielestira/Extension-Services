# export_data.py
import os
import sys
import django

# Adjust this to match your project name if different
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_system.settings')
django.setup()

from django.core import serializers
from django.apps import apps

# Get all models except the ones we want to exclude
all_models = []
for model in apps.get_models():
    app_label = model._meta.app_label
    model_name = model._meta.model_name
    
    # Skip contenttypes and auth.permission
    if app_label == 'contenttypes':
        continue
    if app_label == 'auth' and model_name == 'permission':
        continue
    
    all_models.append(model)

# Get all objects from these models
objects_to_serialize = []
for model in all_models:
    objects_to_serialize.extend(model.objects.all())

print(f"Exporting {len(objects_to_serialize)} objects from {len(all_models)} models...")

# Serialize with UTF-8 encoding
with open('full_data.json', 'w', encoding='utf-8') as f:
    serializers.serialize(
        'json',
        objects_to_serialize,
        indent=2,
        use_natural_foreign_keys=True,
        use_natural_primary_keys=True,
        stream=f
    )

print("✓ Successfully exported to full_data.json")
print(f"✓ File size: {os.path.getsize('full_data.json')} bytes")