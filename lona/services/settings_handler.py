import os
from django.conf import settings
from fastapi import HTTPException

# Ensure DJANGO_SETTINGS_MODULE is set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings.base")  # Replace 'mysite.settings' with your actual settings module

def get_all_settings():
    settings_dict = {}
    for key in dir(settings):
        if not key.startswith('_'):  # Skip private attributes
            try:
                settings_dict[key] = getattr(settings, key)
            except Exception as e:
                # Include the error message in the result for the problematic setting
                settings_dict[key] = f"Error: {str(e)}"
    return settings_dict

def get_setting(setting_name: str):
    try:
        return {setting_name: getattr(settings, setting_name)}
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"Setting '{setting_name}' not found.")

def update_setting(setting_name: str, value):
    if hasattr(settings, setting_name):
        setattr(settings, setting_name, value)
        return {setting_name: value}
    else:
        raise HTTPException(status_code=404, detail=f"Setting '{setting_name}' not found.")

def get_setting_value(setting_name: str):
    try:
        return getattr(settings, setting_name, None)
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"Setting '{setting_name}' not found.")