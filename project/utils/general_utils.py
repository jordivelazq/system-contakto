import datetime


class GetDataTime():
    """
    This class is used to get the current date and time.
    """
    now = datetime.datetime.now()
    year = '{:02d}'.format(now.year)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    day_month_year = '{}/{}/{}'.format(day, month, year)
    hora = '{}:{}'.format(hour, minute)
    fecha_hora = '{} {}'.format(day_month_year, hora)

    def get_current_date_time(self):
        """
        This method is used to get the current date and time.
        :return: current date and time
        """
        return self.now

    def get_current_date(self):
        """
        This method is used to get the current date.
        :return: current date
        """
        return self.now.date()

    def get_current_time(self):
        """
        This method is used to get the current time.
        :return: current time
        """
        return self.now.time()

    def get_current_date_time_in_format(self):
        """
        This method is used to get the current date and time in the specified format.
        :param format: format of the date and time
        :return: current date and time in the specified format
        """

        return str(self.fecha_hora)

    def get_current_date_in_format(self, format):
        """
        This method is used to get the current date in the specified format.
        :param format: format of the date
        :return: current date in the specified format
        """
        return str(self.day_month_year)

    def get_current_time_in_format(self, format):
        """
        This method is used to get the current time in the specified format.
        :param format: format of the time
        :return: current time in the specified format
        """
        return str(self.hora)


class GetUsersInGroup():
    """
    This class is used to get the users in a group.
    """
    def get_users_in_group(self, group_name):
        """
        This method is used to get the users in a group.
        :param group_name: name of the group
        :return: users in the group
        """
        from django.contrib.auth.models import Group
        group = Group.objects.get(name=group_name)
        return group.user_set.all()


class CreateGroupMessaje():
    """
    This class is used to create a group message.
    """
    def create_group_message(self, group_name, investigacion_id):
        """
        This method is used to create a group message.
        :param group_name: name of the group
        :param message: message to be sent
        :return: group message
        """
        from django.contrib.auth.models import Group
        from app.core.models import UserMessage
        group = Group.objects.get(name=group_name)
        users = group.user_set.all()

        if group_name == "Coord. de Atención a Clientes":
            title = 'Se ha creado la investigación con el id: {}'.format(investigacion_id)
            message = 'Le invitamos a que revise la investigación con el id: {}, y empezar el proceso'.format(investigacion_id)
            link = '/investigaciones/investigaciones/detail/{}/'.format(investigacion_id)
        elif group_name == "Cobranzas":
            title = 'Se ha creado la investigación con el id: {}'.format(investigacion_id)
            message = 'Le invitamos a realizar el pago investigación con el id: {}, y enviar cobro al cliente'.format(investigacion_id)
            link = '/cobranza/facturas/detail/{}/'.format(investigacion_id)

        for user in users:
            UserMessage.objects.create(message=message, user=user, title=title, link=link)


class CreateGroupMessajeInd():
    """
    This class is used to create a group message.
    """
    def create_group_message(self, group_name, investigacion_id, title, message, link):
        """
        This method is used to create a group message.
        :param group_name: name of the group
        :param message: message to be sent
        :return: group message
        """
        from django.contrib.auth.models import Group
        from app.core.models import UserMessage
        group = Group.objects.get(name=group_name)
        users = group.user_set.all()

        for user in users:
            UserMessage.objects.create(message=message, user=user, title=title, link=link)
