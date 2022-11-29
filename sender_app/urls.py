from django.conf.urls import url


from . import views

app_name = 'sender_app'

urlpatterns = [
    url(r'^$', views.add_new_client, name='client_new'),
    url(r'^birth/', views.send_birthday, name='send_birthday'),
    url(r'^birth_async/', views.send_birthday_async, name='send_birthday_async'),
    url(r"^email/tr-(?P<key>.*)\.png$", views.email_seen, name="email_seen")
]
