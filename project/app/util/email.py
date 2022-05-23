# from django.core.mail import EmailMultiAlternatives
# import sendgrid
from django.core.mail import EmailMultiAlternatives, EmailMessage
import os
import requests

class EmailHandler:
  '''
    Class helper to send emails. For now it works with sendgrid
  '''

  def sendEmail(self, data):
    '''
    Function to send the email with sendgrid
    @param {object} data object with the email data
    '''
    try:
        # sg = sendgrid.SendGridClient(os.environ['SENDGRID_API_KEY'])
        # message = sendgrid.Mail(to=data['to'], subject=data['subject'], html=data['html_content'], text=data['text_content'], from_email=data['from_email'])
        # status, msg = sg.send(message)

        subject, from_email, to = data['subject'], data['from_email'], data['to']

        bcc = ['estudios@contakto.mx']
        text_content = ''
        html_content = data['html_content']
        msg = EmailMultiAlternatives(subject, text_content, from_email, to, bcc=bcc)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        payload = {
          'to': data['to'],
          'subject': data['subject'],
          'from': data['from_email'],
          'size': len(data['html_content']),
          'account': 'contaktoapp',
        }
        requests.post(os.environ['EMAIL_LOG_URL'], json=payload)

        return True
    except:
        return False

'''
from django.core.mail import EmailMultiAlternatives, EmailMessage
subject, from_email, to = 'Prueba desde subject', 'estudios@contakto.mx', ['hernan.ramirez@gmail.com',]

bcc = ['estudios@contakto.mx']
text_content = 'demo text'
html_content = '<b>ok...</b> ok'
msg = EmailMultiAlternatives(subject, text_content, from_email, to, bcc=bcc)
msg.attach_alternative(html_content, "text/html")
msg.send()



message = EmailMessage(subject, html_content, from_email, to, bcc=bcc)
message.content_subtype = "html"
message.send()
'''