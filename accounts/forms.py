from django import forms
from .models import Profile

class BackgroundUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['background_image']

    def clean_background_image(self):
        image = self.cleaned_data.get('background_image')

        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB ).")

            if not image.content_type in ["image/jpeg", "image/png"]:
                raise forms.ValidationError("Only JPEG and PNG formats are supported.")

        return image
