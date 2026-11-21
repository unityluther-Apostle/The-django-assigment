from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import AnnouncementForm
from .models import Announcement, ReadStatus


@login_required
def feed_view(request):
    announcements = Announcement.objects.all()

    read_ids = set(
        ReadStatus.objects.filter(student=request.user)
        .values_list("announcement_id", flat=True)
    )

    news = announcements.filter(category="news")
    entertainment = announcements.filter(category="entertainment")

    context = {
        "news": news,
        "entertainment": entertainment,
        "read_ids": read_ids,
    }
    return render(request, "notifications/feed.html", context)


@login_required
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    ReadStatus.objects.get_or_create(
        student=request.user,
        announcement=announcement,
    )

    return render(
        request,
        "notifications/announcement_detail.html",
        {"announcement": announcement},
    )


class AdminDashboardView(UserPassesTestMixin, ListView):
    model = Announcement
    template_name = "notifications/manage_dashboard.html"
    context_object_name = "announcements"

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get("category")

        if category in ("news", "entertainment"):
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_category"] = self.request.GET.get("category", "all")
        return context


class AnnouncementCreateView(UserPassesTestMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "notifications/announcement_form.html"
    success_url = reverse_lazy("notifications:manage_dashboard")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request,
            f"Announcement '{form.instance.title}' created.",
        )
        return super().form_valid(form)


class AnnouncementUpdateView(UserPassesTestMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "notifications/announcement_form.html"
    success_url = reverse_lazy("notifications:manage_dashboard")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Announcement '{form.instance.title}' updated.",
        )
        return super().form_valid(form)


class AnnouncementDeleteView(UserPassesTestMixin, DeleteView):
    model = Announcement
    template_name = "notifications/announcement_confirm_delete.html"
    success_url = reverse_lazy("notifications:manage_dashboard")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        title = self.object.title
        messages.success(
            self.request,
            f"Announcement '{title}' deleted.",
        )
        return super().form_valid(form)
