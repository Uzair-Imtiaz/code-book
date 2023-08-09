""" This module contains Django views for handling project-related actions """

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from core.forms import ProjectForm, ReviewForm
from core.models import Project, Review


class AddOrEditProjectView(LoginRequiredMixin, View):
    """ A view to handle adding new projects by authenticated users """

    def get(self, request, pk=None):
        """ Handle HTTP GET request for adding a new project or editing ann existing one """

        page = 'Add Project'

        if pk:
            project = get_object_or_404(Project, pk=pk, user=request.user)
            form = ProjectForm(instance=project)
        else:
            form = ProjectForm()

        context = {
            'page': page,
            'form': form,
        }
        return render(request, 'core/project_form.html', context)

    def post(self, request, pk=None):
        """ Handle HTTP POST request for adding a new project or editing an existing one"""

        user = request.user

        if pk:
            project = get_object_or_404(Project, pk=pk, user=user)
            form = ProjectForm(request.POST, request.FILES, instance=project)
        else:
            form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = user
            project.save()
            tags_ids = request.POST.getlist('skills')
            project.skills.set(tags_ids)
            messages.success(request, 'Project added/edited!')
            return redirect(reverse('core:project', kwargs={'pk': project.id}))

        else:
            messages.error(request, 'An error occurred!')
            return render(request, 'core/project_form.html')


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    """ A view to handle the deletion of a project instance """

    model = Project
    success_url = reverse_lazy('core:projects')


class AddReview(LoginRequiredMixin, CreateView):
    """ A view to handle the addition of new reviews by authenticated users """

    model = Review
    form_class = ReviewForm
    template_name = 'core/single_project.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        project_id = self.kwargs.get('pk')

        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                form.instance.project = project
            except Project.DoesNotExist:
                pass
            form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:project', args=[self.kwargs['pk']])


class ProjectsView(ListView):
    """ A view to display list of projects """

    page = 'Projects'
    model = Project
    template_name = 'core/projects.html'
    context_object_name = 'projects'


class SingleProjectView(DetailView):
    """ A view to display a specific project """

    model = Project
    template_name = 'core/single_project.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['project'] = project
        context['page'] = project.title
        context['tags'] = project.skills.all()
        context['reviews'] = project.review_set.all()
        context['user_reviewed'] = Review.objects.filter(project=project, user_id=self.request.user.pk).exists()
        up_votes = Review.objects.filter(project=project, vote='Up').count()
        try:
            ratio = (up_votes * 100) // Review.objects.filter(project=project).count()
        except ZeroDivisionError:
            ratio = 0

        context['votes_ratio'] = ratio
        context['form'] = ReviewForm()
        return context
