import logging

db_default_formatter = logging.Formatter()


class DatabaseLogHandler(logging.Handler):

    # TODO: gevent pool
    def emit(self, record):

        from mce_django_app.models.logs import StatusLog
        #from django.conf import settings

        #DJANGO_DB_LOGGER_ENABLE_FORMATTER = getattr(
        #    settings, 'DJANGO_DB_LOGGER_ENABLE_FORMATTER', False
        #)
        DJANGO_DB_LOGGER_ENABLE_FORMATTER = False

        trace = None

        if record.exc_info:
            trace = db_default_formatter.formatException(record.exc_info)

        if DJANGO_DB_LOGGER_ENABLE_FORMATTER:
            msg = self.format(record)
        else:
            msg = record.getMessage()

        kwargs = {
            'logger_name': record.name,
            'level': record.levelno,
            'msg': msg,
            'trace': trace,
        }

        StatusLog.objects.create(**kwargs)

    def format(self, record):
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = db_default_formatter

        if type(fmt) == logging.Formatter:
            record.message = record.getMessage()

            if fmt.usesTime():
                record.asctime = fmt.formatTime(record, fmt.datefmt)

            # ignore exception traceback and stack info

            return fmt.formatMessage(record)
        else:
            return fmt.format(record)
