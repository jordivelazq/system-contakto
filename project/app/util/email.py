# from django.core.mail import EmailMultiAlternatives
# import sendgrid
from django.core.mail import EmailMultiAlternatives
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.urls import reverse
from ..investigacion.models import Investigacion

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
        
        # se elimina, al parecer es por el tema del uso del SendGrid
        # requests.post(os.environ['EMAIL_LOG_URL'], json=payload)

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

''' New method to send email'''

def send_email(inv:Investigacion, to=None, cc=None):
    
    from_address = settings.EMAIL_HOST_USER
    to_address = 'tabasco.dev@gmail.com'

    if inv.cliente_solicitud_candidato.cliente_solicitud.cliente.email:
       to_address = inv.cliente_solicitud_candidato.cliente_solicitud.cliente.email

    if to:
       to_address = to

    mime_message = MIMEMultipart('alternative')
    mime_message["From"] = from_address
    mime_message["To"] = to_address

    if cc:
        mime_message['Cc'] = cc # "email1, email2" <-- format
        to_address = [to_address] + cc.split(',') # [main] + [email1, email2] <-- format

    mime_message["Subject"] = "CONTAKTO"
    url = ""
    if inv.tipo_investigacion.first().tipo_investigacion == 'Laboral':
       url = settings.HOST_SERVER + reverse("print_reporte_laboral", kwargs={'investigacion_id': inv.pk})
    elif inv.tipo_investigacion.first().tipo_investigacion == 'Socioeconómico':
      url = settings.HOST_SERVER + reverse("print_reporte_socioeconomico", kwargs={'investigacion_id': inv.pk})

    elif inv.tipo_investigacion.first().tipo_investigacion == 'Visita domiciliaria':
      url = settings.HOST_SERVER + reverse("print_reporte_visita_domiciliaria", kwargs={'investigacion_id': inv.pk})

    elif inv.tipo_investigacion.first().tipo_investigacion == 'Validación de demandas':
      url = settings.HOST_SERVER + reverse("print_reporte_validacion_demandas", kwargs={'investigacion_id': inv.pk})
    else:
       pass

    plantilla = '''
    <!doctype html>
    <html>
      <head>
        <meta name="viewport" content="width=device-width">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Solicitud | CONTAKTO</title>
      <style>
    @media only screen and (max-width: 620px) {{
      table[class=body] h1 {{
        font-size: 28px !important;
        margin-bottom: 10px !important;
      }}

      table[class=body] p,
    table[class=body] ul,
    table[class=body] ol,
    table[class=body] td,
    table[class=body] span,
    table[class=body] a {{
        font-size: 16px !important;
      }}

      table[class=body] .wrapper,
    table[class=body] .article {{
        padding: 10px !important;
      }}

      table[class=body] .content {{
        padding: 0 !important;
      }}

      table[class=body] .container {{
        padding: 0 !important;
        width: 100% !important;
      }}

      table[class=body] .main {{
        border-left-width: 0 !important;
        border-radius: 0 !important;
        border-right-width: 0 !important;
      }}

      table[class=body] .btn table {{
        width: 100% !important;
      }}

      table[class=body] .btn a {{
        width: 100% !important;
      }}
      
      table[class=body] .img-responsive {{
        height: auto !important;
        max-width: 100% !important;
        width: auto !important;
      }}
    }}
    @media all {{
      .ExternalClass {{
        width: 100%;
    }}
      .ExternalClass,
    .ExternalClass p,
    .ExternalClass span,
    .ExternalClass font,
    .ExternalClass td,
    .ExternalClass div {{
        line-height: 100%;
    }}
      .apple-link a {{
        color: inherit !important;
        font-family: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
        line-height: inherit !important;
        text-decoration: none !important;
    }}
      .btn-primary table td:hover {{
        background-color: #d50707 !important;
    }}
      .btn-primary a:hover {{
        background-color: #d50707 !important;
        border-color: #d50707 !important;
    }}
    }}
    </style></head>
      <body class style="background-color: #eaebed; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; background-color: #eaebed; width: 100%;" width="100%" bgcolor="#eaebed">
          <tr>
            <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">&nbsp;</td>
            <td class="container" style="font-family: sans-serif; font-size: 14px; vertical-align: top; display: block; max-width: 580px; padding: 10px; width: 580px; Margin: 0 auto;" width="580" valign="top">
              <div class="header" style="padding: 20px 0;">
                <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; width: 100%;">
                  <tr>
                    <td class="align-center" width="100%" style="font-family: sans-serif; font-size: 14px; vertical-align: top; text-align: center;" valign="top" align="center">
                      <a href="https://contakto.mx" style="color: #d50707; text-decoration: underline;"><img src="https://web.contakto.mx/static/images/logo-nuevo.png" height="40" alt="CONTAKTO" style="border: none; -ms-interpolation-mode: bicubic; max-width: 100%;"></a>
                    </td>
                  </tr>
                </table>
              </div>
              <div class="content" style="box-sizing: border-box; display: block; Margin: 0 auto; max-width: 580px; padding: 10px;">

                <!-- START CENTERED WHITE CONTAINER -->
                <span class="preheader" style="color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;">Bienvenido</span>
                <table role="presentation" class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; background: #ffffff; border-radius: 3px; width: 100%;" width="100%">

                  <!-- START MAIN CONTENT AREA -->
                  <tr>
                    <td class="wrapper" style="font-family: sans-serif; font-size: 14px; vertical-align: top; box-sizing: border-box; padding: 20px;" valign="top">
                      <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; width: 100%;" width="100%">
                        <tr>
                          <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">
                            <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 15px;">
                              <h3 style="text-align:center">Investigación completada</h3>
                                <hr>
                                {0}
                            </p>
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; box-sizing: border-box; width: 100%;" width="100%">
                              <tbody>
                                <tr>
                                  <td align="center" style="font-family: sans-serif; font-size: 14px; vertical-align: top; padding-bottom: 15px;" valign="top">
                                    <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: auto; width: auto;" width="auto">
                                      <tbody>
                                        <tr>
                                          <td style="font-family: sans-serif; font-size: 14px; vertical-align: top; border-radius: 5px; text-align: center; background-color: #d50707;" valign="top" align="center" bgcolor="#d50707"> <a href="{1}" target="_blank" style="border: solid 1px #d50707; border-radius: 5px; box-sizing: border-box; cursor: pointer; display: inline-block; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-decoration: none; background-color: #d50707; border-color: #d50707; color: #ffffff;"> Descargar estudio {2}</a> </td>
                                        </tr>
                                      </tbody>
                                    </table>
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                            <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 15px;">Gracias por su preferencia</p>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>

                <!-- END MAIN CONTENT AREA -->
                </table>

                <!-- START FOOTER -->
                <div class="footer" style="clear: both; Margin-top: 10px; text-align: center; width: 100%;">
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; width: 100%;" width="100%">
                    <tr>
                      <td class="content-block" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; color: #9a9ea6; font-size: 12px; text-align: center;" valign="top" align="center">
                        <span class="apple-link" style="color: #9a9ea6; font-size: 12px; text-align: center;">No olvides visitar nuestro sitio web</span>
                        <br> And <a href="https://contakto.mx" style="text-decoration: underline; color: #9a9ea6; font-size: 12px; text-align: center;">Ir al sitio</a> aquí.
                      </td>
                    </tr>
                    <tr>
                      <td class="content-block powered-by" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; color: #9a9ea6; font-size: 12px; text-align: center;" valign="top" align="center">
                        Powered by <a href="https://contakto.mx" style="color: #9a9ea6; font-size: 12px; text-align: center; text-decoration: none;">Contakto</a>.
                      </td>
                    </tr>
                  </table>
                </div>
                <!-- END FOOTER -->

              <!-- END CENTERED WHITE CONTAINER -->
              </div>
            </td>
            <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">&nbsp;</td>
          </tr>
        </table>
      </body>
    </html>
    '''.format(f'''
       <h5>Empresa: {inv.compania.nombre }</h5>
        <hr>
        <h5>Puesto: {inv.puesto}</h5>
        <hr>
        <h5>
        Candidato : {inv.candidato.nombre} {inv.candidato.apellido}
        </h5>''',
        url, 
        inv.tipo_investigacion.first().tipo_investigacion
        )
    
    message = MIMEText(plantilla, 'html')
    mime_message.attach(message)
    smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    smtp.sendmail(from_address, to_address, mime_message.as_string())
    smtp.quit()