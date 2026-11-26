from django.db import migrations

def create_smart_devices(apps, schema_editor):
    # We use apps.get_model to avoid importing the model directly
    SmartHomeDevice = apps.get_model('vitals', 'SmartHomeDevice')
    
    # Check if they already exist to avoid duplicates on redeploy
    if not SmartHomeDevice.objects.filter(device_id='light1').exists():
        SmartHomeDevice.objects.create(name="Living Room Light", device_id="light1")
    if not SmartHomeDevice.objects.filter(device_id='fan1').exists():
        SmartHomeDevice.objects.create(name="Bedroom Fan", device_id="fan1")

class Migration(migrations.Migration):
    dependencies = [
        ('vitals', '0004_smarthomedevice'),
    ]
    

    operations = [
        migrations.RunPython(create_smart_devices),
    ]