from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email(tipo, data):

    bcc = ['hr@hernanramirez.info']
    email_from = 'hr@hernanramirez.info'

    message = None
    subject = None
    from_email = None
    to = None

    if tipo == "notificacion_coordinador_ejecutivo":
        message = render_to_string('mail/clientes/notificacion_coordinador_ejecutivo.html', data)

        subject, from_email = "Estimado(a) Coordinador de ejecutivos, se ha generdo una nueva solicitud", email_from
        to = data['email_coordinadores_de_ejecutivos']

    if tipo == "notificacion_coordinador_visita":
        message = render_to_string('mail/coordinadores/notificacion_coordinador_visita.html', data)

        subject, from_email = "Estimado(a) Coordinador de visita, se ha generdo una nueva solicitud", email_from
        to = data['email_coordinadores_de_visita']

    text_content = ''
    html_content = message
    msg = EmailMultiAlternatives(subject, text_content, from_email, to, bcc=bcc)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

