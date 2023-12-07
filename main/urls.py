from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import ClientListView, MessageCreateView, MessageListView, MessageDetailView, MessageUpdateView, \
    MessageDelete, IndexView, MailingCreateView, ClientCreateView, MailingListView, ClientDetailView, ClientUpdateView, \
    ClientDelete, MailingDetailView, MailingUpdateView, MailingDelete, LogListView, MailingUpdateManagerView, \
    MailingSendMessageView

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(60)(IndexView.as_view()), name='index'),

    path('clients/create_client/', ClientCreateView.as_view(), name='create_client'),
    path('clients/clients_list/', ClientListView.as_view(), name='clients_list'),
    path('clients/view_client/<int:pk>/', ClientDetailView.as_view(), name='view_client'),
    path('clients/edit_client/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('clients/delete_client/<int:pk>/', ClientDelete.as_view(), name='delete_client'),

    path('messages/create_message/', MessageCreateView.as_view(), name='create_message'),
    path('messages/messages_list/', MessageListView.as_view(), name='messages_list'),
    path('messages/view_message/<int:pk>/', MessageDetailView.as_view(), name='view_message'),
    path('messages/edit_message/<int:pk>/', MessageUpdateView.as_view(), name='edit_message'),
    path('messages/delete_message/<int:pk>/', MessageDelete.as_view(), name='delete_message'),

    path('mailings/create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailings/mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/view_mailing/<int:pk>/', MailingDetailView.as_view(), name='view_mailing'),
    path('mailings/edit_mailing_manager/<int:pk>/', MailingUpdateManagerView.as_view(), name='edit_mailing_manager'),
    path('mailings/manager_edit_mailing/<int:pk>/', MailingUpdateManagerView.as_view(), name='manager_edit_mailing'),
    path('mailings/delete_mailing/<int:pk>/', MailingDelete.as_view(), name='delete_mailing'),
    path('mailings/send_mailing/<int:pk>/', MailingSendMessageView.as_view(), name='send_mailing'),

    path('log/log_list/', LogListView.as_view(), name='log_list'),
]