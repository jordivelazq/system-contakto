# from django.core.mail import EmailMultiAlternatives
import sendgrid
import os

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
        message = sendgrid.Mail(to=data['to'], subject=data['subject'], html=data['html_content'], text=data['text_content'], from_email=data['from_email'], bcc=["info@mintitmedia.com"])
        status, msg = sg.send(message)
        return True
    except:
        return False
