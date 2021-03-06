from django.views.generic import DetailView, ListView

from braces.views import LoginRequiredMixin

from affiliates.links.models import LeaderboardStanding, Link


class LinkDetailView(LoginRequiredMixin, DetailView):
    template_name = 'links/detail.html'
    context_object_name = 'link'

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)


class LinkReferralView(DetailView):
    template_name = 'links/referral.html'
    model = Link
    context_object_name = 'link'


class LeaderboardView(ListView):
    queryset = LeaderboardStanding.objects.filter(metric='link_clicks').order_by('ranking')
    template_name = 'links/leaderboard.html'
    context_object_name = 'standings'
    paginate_by = 10
