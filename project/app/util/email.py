# from django.core.mail import EmailMultiAlternatives
import sendgrid
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
        sg = sendgrid.SendGridClient(os.environ['SENDGRID_API_KEY'])
        message = sendgrid.Mail(to=data['to'], subject=data['subject'], html=data['html_content'], text=data['text_content'], from_email=data['from_email'])
        status, msg = sg.send(message)

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
