from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

def user_background_path(instance, filename):
    return f'user_backgrounds/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    background_image = models.ImageField(upload_to=user_background_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Get previous image (if any)
        try:
            old_instance = Profile.objects.get(pk=self.pk)
            if old_instance.background_image and old_instance.background_image != self.background_image:
                old_instance.background_image.delete(save=False)
        except Profile.DoesNotExist:
            pass

        # Resize uploaded image
        if self.background_image:
            try:
                img = Image.open(self.background_image)
                img = img.convert('RGB')
                img = img.resize((1920, 1080))

                buffer = BytesIO()
                img.save(buffer, format='JPEG')
                buffer.seek(0)

                file_name = os.path.basename(self.background_image.name)
                self.background_image.save(file_name, ContentFile(buffer.read()), save=False)
            except Exception as e:
                print("Image processing failed:", e)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"
