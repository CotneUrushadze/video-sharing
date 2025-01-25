from django.shortcuts import render, get_object_or_404, reverse
from django.views import View
from django.views.generic.edit import UpdateView
from profiles.models import *
from videos.models import *


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        videos = Video.objects.all().filter(uploader=pk).order_by('-date_posted')
        user = request.user

        context = {
            'profile': profile,
            'videos': videos,
            'user.profile': user,
        }

        return render(request, 'profiles/profiles.html', context)
    


class UpdateProfile(UpdateView):
    model = Profile
    fields = ['name', 'location', 'image']
    template_name = 'profiles/update_profile.html'

    def form_valid(self, form):
        if not form.instance.image:
            form.instance.image = 'uploads/profile_pics/default.jpg'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})