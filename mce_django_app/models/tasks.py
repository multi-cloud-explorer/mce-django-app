from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from jsonfield import JSONField

from mce_django_app import constants
from mce_django_app import utils
from mce_django_app.models.common import BaseModel


class WorkerTask(BaseModel):
    """Task running."""

    task_id = models.CharField(
        max_length=getattr(
            settings,
            'DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH',
            255
        ),
        unique=True,
        verbose_name=_('Task ID'),
        help_text=_('Celery ID for the Task that was run'))

    task_name = models.CharField(
        null=True, max_length=255, db_index=True,
        verbose_name=_('Task Name'),
        help_text=_('Name of the Task which was run'))

    task_args = models.TextField(
        null=True,
        verbose_name=_('Task Positional Arguments'),
        help_text=_('JSON representation of the positional arguments '
                    'used with the task'))

    task_kwargs = models.TextField(
        null=True,
        verbose_name=_('Task Named Arguments'),
        help_text=_('JSON representation of the named arguments '
                    'used with the task'))

    status = models.CharField(
        max_length=50, default=constants.TaskState.PENDING, db_index=True,
        choices=constants.TaskState.choices,
        verbose_name=_('Task State'),
        help_text=_('Current state of the task being run'))

    worker = models.CharField(
        max_length=100, db_index=True, default=None, null=True, blank=True,
        verbose_name=_('Worker'), help_text=_('Worker that executes the task')
    )

    # content_type = models.CharField(
    #     max_length=128,
    #     verbose_name=_('Result Content Type'),
    #     help_text=_('Content type of the result data'))
    #
    # content_encoding = models.CharField(
    #     max_length=64,
    #     verbose_name=_('Result Encoding'),
    #     help_text=_('The encoding used to save the task result data'))
    #
    result = models.TextField(
        null=True, default=None, editable=False,
        verbose_name=_('Result Data'),
        help_text=_('The data returned by the task.  '
                    'Use content_encoding and content_type fields to read.'))

    # date_created = models.DateTimeField(
    #     auto_now_add=True, db_index=True,
    #     verbose_name=_('Created DateTime'),
    #     help_text=_('Datetime field when the task result was created in UTC'))

    date_done = models.DateTimeField(
        db_index=True, null=True, blank=True,
        verbose_name=_('Completed DateTime'),
        help_text=_('Datetime field when the task was completed in UTC'))

    traceback = models.TextField(
        blank=True, null=True,
        verbose_name=_('Traceback'),
        help_text=_('Text of the traceback if the task generated one'))

    meta = models.TextField(
        null=True, default=None, editable=False,
        verbose_name=_('Task Meta Information'),
        help_text=_('JSON meta information about the task, '
                    'such as information on child tasks'))

    retry = models.IntegerField(
                            verbose_name=_("Task Retries"),
                            default=0)

    duration = models.FloatField(
                            verbose_name=_("Run duration"),
                            default=0.0)

    #objects = managers.TaskResultManager()

    class Meta:
        """Table information."""

        ordering = ['-date_done']

        verbose_name = _('task result')
        verbose_name_plural = _('task results')

    def as_dict(self):
        return {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'task_args': self.task_args,
            'task_kwargs': self.task_kwargs,
            'status': self.status,
            'result': self.result,
            'date_done': self.date_done,
            'traceback': self.traceback,
            'meta': self.meta,
            'worker': self.worker
        }

    def __str__(self):
        return '<Task: {0.task_id} ({0.status})>'.format(self)


# class TaskResult(BaseModel):
#     """Record tasks result
#
#     Django-RQ n'enregistre pas les résultats dans un model
#     """
#
#     """
#     func_name
#     func_args
#     func_kwargs
#     parent (if depend_on)
#     """
#
#     task_id = models.CharField(
#                             max_length=255,
#                             unique=True,
#                             editable=False)
#
#     state = models.CharField(
#                             max_length=255,
#                             default=constants.TaskState.UNKNOW,
#                             choices=constants.TaskState.choices,
#                             verbose_name=_("Task State"))
#
#     message = models.TextField(
#                             verbose_name=_("Message"),
#                             null=True)
#
#     traceback = models.TextField(
#                             _("Trace error"),
#                             null=True)
#
#
#     exit_code = models.IntegerField(
#                             verbose_name=_("Exit code"),
#                             null=True)
#
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#
#     object_id = models.PositiveIntegerField()
#
#     content_object = GenericForeignKey(
#         'content_type', 'object_id', for_concrete_model=False
#     )
#
#     def __str__(self):
#         return f"{self.task.name} ({self.state})"
#
#     class Meta:
#         get_latest_by = 'created'
#         ordering = ['-created']
#
#
