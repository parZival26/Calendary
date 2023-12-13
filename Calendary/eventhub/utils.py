# utils.py
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def enviar_correo(destinatario, asunto, cuerpo):
    correo = EmailMessage(asunto, cuerpo, to=[destinatario])
    correo.send()
