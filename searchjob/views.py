import random

from django.contrib.messages.views import SuccessMessageMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count, Q
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import BaseFormView, DeleteView, UpdateView, CreateView

from .forms import ResponseForm, VacancyForm, CompanyForm
from .models import *
from .mixins import UserHasCompany, UserHasNotCompany


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialies'] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        context['companies'] = Company.objects.annotate(vacancies_count=Count('vacancies'))
        if len(list(Company.objects.annotate(vacancies_count=Count('vacancies')))) >= 8:
            context['companies'] = random.sample(list(Company.objects.annotate(vacancies_count=Count('vacancies'))), 8)
        return context


class VacanciesView(ListView):
    model = Vacancy
    queryset = Vacancy.objects.select_related('company')
    template_name = 'vacancies.html'
    context_object_name = 'vacancies'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_count'] = Vacancy.objects.count()
        return context


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.filter(company=self.kwargs['pk']).select_related('specialty')
        return context


class CategoryView(ListView):
    model = Vacancy
    template_name = 'vacancies.html'
    context_object_name = 'vacancies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialty'] = get_object_or_404(Specialty, code=self.kwargs['code'])
        return context

    def get_queryset(self):
        return Vacancy.objects.filter(specialty__code=self.kwargs['code']).select_related('specialty')


class VacancyDetailView(SuccessMessageMixin, BaseFormView, DetailView):
    template_name = 'vacancy.html'
    queryset = Vacancy.objects.select_related('company')
    context_object_name = 'vacancy'
    form_class = ResponseForm
    success_url = 'send/'

    # def get_success_url(self):
    #     return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['already_respond'] = (
            Response.objects.filter(
                vacancy_id=self.kwargs['pk'],
                user_id=self.request.user.pk,
            )
                .exists()
        )
        return context

    def form_valid(self, form):
        application: Response = form.save(commit=False)
        application.vacancy_id = self.kwargs['pk']
        application.user_id = self.request.user.pk
        application.full_clean()
        application.save()
        return super().form_valid(form)


class SearchView(ListView):
    model = Vacancy
    template_name = "search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            object_list = Vacancy.objects.filter(
                Q(skills__icontains=query) | Q(title_vacancy__icontains=query))
        else:
            object_list = Vacancy.objects.all().select_related('specialty')
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "")
        context["search_string"] = query
        return context


def send_view(request: WSGIRequest, id):
    try:
        vacancies = Vacancy.objects.get(id=id)
    except Vacancy.DoesNotExist:
        raise Http404
    return render(request, 'send.html', context={
        'vacancies': vacancies,
    })


class CompanyStartView(UserHasNotCompany, TemplateView):
    template_name = 'start.html'


class CompanyCreateView(UserHasNotCompany, SuccessMessageMixin, CreateView):
    template_name = 'edit_company.html'
    form_class = CompanyForm
    success_message = 'Компания успешно создана'
    success_url = reverse_lazy('edit_company')

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.pk
        return super().form_valid(form)


class CompanyEditView(UserHasCompany, SuccessMessageMixin, UpdateView):
    template_name = 'edit_company.html'
    form_class = CompanyForm
    success_message = 'Информация обновлена'
    success_url = reverse_lazy('edit_company')

    def get_object(self, queryset=None):
        return self.request.user.company


class VacanciesListView(ListView):
    model = Vacancy
    template_name = 'my_vacancies.html'
    context_object_name = 'my_vacancies'
    paginate_by = 5

    def get_queryset(self):
        return Vacancy.objects.filter(company=self.request.user.pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['response'] = Response.objects.all()
        return context



class VacancyCreateView(CreateView):
    template_name = 'create_vacancy.html'
    form_class = VacancyForm
    success_url = reverse_lazy('my_vacancies')

    def form_valid(self, form):
        form.instance.company_id = self.request.user.pk
        return super().form_valid(form)


class VacancyEditView(SuccessMessageMixin, UpdateView, ListView):
    model = Response
    template_name = 'edit_vacancy.html'
    success_message = 'Информация обновлена'
    form_class = VacancyForm

    def get_queryset(self):
        return Vacancy.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.filter(vacancy=self.kwargs['pk'])
        context['vacancy'] = Vacancy.objects.filter(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("edit_vacancy", kwargs={"pk": pk})


class VacancyDeleteView(DeleteView):
    model = Vacancy
    template_name = 'delete.html'
    success_url = reverse_lazy('my_vacancies')

    def get_queryset(self):
        return Vacancy.objects.filter(pk=self.kwargs['pk'])
