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
