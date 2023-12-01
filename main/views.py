from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView

from main.forms import MailingForm, ClientForm, MessageForm
from main.models import Client, Message, Mailing


class IndexView(TemplateView):
    """Класс отображения главной страницы сервиса"""

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        return context


class ClientCreateView(CreateView):
    """Контроллер для создания нового клиента - получателя рассылки"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:clients_list')


class ClientListView(ListView):
    """Контроллер для просмотра списка клиентов"""

    model = Client


class ClientDetailView(DetailView):
    """Контроллер для детального просмотра клиента"""

    model = Client


class ClientUpdateView(UpdateView):
    """Контроллер для редактирования клиента"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:clients_list')


class ClientDelete(DeleteView):
    """Контроллер для удаления клиента"""

    model = Client
    success_url = reverse_lazy('main:clients_list')


class MessageCreateView(CreateView):
    """Контроллер для создания нового сообщения"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:messages_list')


class MessageListView(ListView):
    """Контроллер для просмотра списка сообщений"""

    model = Message


class MessageDetailView(DetailView):
    """Контроллер для детального просмотра сообщения"""

    model = Message


class MessageUpdateView(UpdateView):
    """Контроллер для редактирования сообщения"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:messages_list')


class MessageDelete(DeleteView):
    """Контроллер для удаления сообщения"""

    model = Message
    success_url = reverse_lazy('main:messages_list')


class MailingCreateView(CreateView):
    """Контроллер для создания новой рассылки"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')


class MailingListView(ListView):
    """Контроллер для просмотра списка рассылок"""

    model = Mailing


class MailingDetailView(DetailView):
    """Контроллер для детального просмотра рассылки"""

    model = Mailing


class MailingUpdateView(UpdateView):
    """Контроллер для редактирования рассылки"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')


class MailingDelete(DeleteView):
    """Контроллер для удаления рассылки"""

    model = Mailing
    success_url = reverse_lazy('main:mailing_list')
