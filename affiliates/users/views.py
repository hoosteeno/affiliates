from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import UpdateView

from tower import ugettext as _

from affiliates.users.forms import EditProfileForm
from affiliates.users.models import UserProfile


class UserProfileView(UpdateView):
    model = UserProfile
    form_class = EditProfileForm
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def post(self, request, *args, **kwargs):
        # Only allow editing of the user if you are logged in as the
        # current user.
        profile = self.get_object()
        if request.user != profile.user:
            # TODO: Add some sort've error message here.
            return redirect(profile)
        else:
            return super(UserProfileView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _('Your profile has been updated!'))
        return super(UpdateView, self).form_valid(form)


def login_required(request):
    messages.warning(request, _('You must be logged in to view that page.'))
    return redirect('base.home')
