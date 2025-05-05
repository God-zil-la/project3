from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BackgroundUploadForm
from django.contrib import messages

@login_required
def upload_background(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = BackgroundUploadForm(request.POST, request.FILES, instance=profile)

        if not request.FILES.get('background_image'):
            messages.error(request, "Please choose a file before uploading.")
            return redirect('upload_background')

        if form.is_valid():
            form.save()
            messages.success(request, "Background image uploaded successfully.")
            return redirect('event_list')
        else:
            messages.error(request, "Failed to upload image. Please check the form.")
    else:
        form = BackgroundUploadForm(instance=profile)

    return render(request, 'accounts/upload_background.html', {'form': form})

