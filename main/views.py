from django.contrib.auth.mixins import LoginRequiredMixin

import random
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView

from blog.models import Blog
from main.forms import MailingForm, ClientForm, MessageForm, MailingUpdateManagerForm
from main.models import Client, Message, Mailing, Log



class IndexView(TemplateView):
    """Класс отображения главной страницы сервиса"""

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        # Получение количества рассылок всего
        total_mailings = Mailing.objects.count()
        context['total_mailings'] = total_mailings

        # Получение количества активных рассылок
        active_mailings = Mailing.objects.filter(is_active=True).count()
        context['active_mailings'] = active_mailings

        # Получение количества уникальных клиентов для рассылок
        unique_clients = Client.objects.count()
        context['unique_clients'] = unique_clients

        # Получение всех статей блога
        all_blogs = list(Blog.objects.all())

        if len(all_blogs) >= 3:
            # Получение трёх случайных статей из блога
            random_blogs = random.sample(all_blogs, 3)
        else:
            # Если количество статей меньше 3, выводим все статьи
            random_blogs = all_blogs

        context['random_blogs'] = random_blogs

        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания нового клиента - получателя рассылки"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:clients_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка клиентов"""

    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('main.can_manager_view'):
            return queryset
        return queryset.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для детального просмотра клиента"""

    model = Client


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования клиента"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:clients_list')


class ClientDelete(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления клиента"""

    model = Client
    success_url = reverse_lazy('main:clients_list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания нового сообщения"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:messages_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка сообщений"""

    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('main.can_manager_view'):
            return queryset
        return queryset.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для детального просмотра сообщения"""

    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования сообщения"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:messages_list')


class MessageDelete(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления сообщения"""

    model = Message
    success_url = reverse_lazy('main:messages_list')


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания новой рассылки"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка рассылок"""

    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('main.can_manager_view'):
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingSendMessageView(LoginRequiredMixin, DetailView):
    """Контроллер для старта рассылки"""

    template_name = 'main/mailing_send_message_successful.html'
    model = Mailing

    def get(self, *args, **kwargs):
        mailing = self.get_object()
        mailing.send()
        return super().get(*args, **kwargs)


class MailingDetailView(DetailView):
    """Контроллер для детального просмотра рассылки"""

    model = Mailing


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования рассылки"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs


class MailingUpdateManagerView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования рассылки менеджером-модератором"""

    template_name = 'main/mailing_manager_form.html'
    model = Mailing
    form_class = MailingUpdateManagerForm
    success_url = reverse_lazy('main:mailing_list')


class MailingDelete(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления рассылки"""

    model = Mailing
    success_url = reverse_lazy('main:mailing_list')


class LogListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка логов рассылок"""

    model = Log

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('main.can_manager_view'):
            return queryset
        return queryset.filter(mailing__owner=self.request.user)
