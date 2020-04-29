from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from jsonfield import JSONField

from mce_django_app import constants
from mce_django_app import utils
from mce_django_app.models.common import BaseModel

class TaskResult(BaseModel):
    """Record tasks result
    
    Django-RQ n'enregistre pas les résultats dans un model
    """

    """
    func_name
    func_args
    func_kwargs
    parent (if depend_on)
    """

    task_id = models.CharField(
                            max_length=255,
                            unique=True,
                            editable=False)

    state = models.CharField(
                            max_length=255,
                            default=constants.TaskState.UNKNOW,
                            choices=constants.TaskState.choices,
                            verbose_name=_("Task State"))

    message = models.TextField(
                            verbose_name=_("Message"), 
                            null=True)

    traceback = models.TextField(
                            _("Trace error"), 
                            null=True)

    output = JSONField(
                            default={},
                            verbose_name=_("Sortie"),
                            blank=True, null=True)

    exit_code = models.IntegerField(
                            verbose_name=_("Exit code"), 
                            null=True)

    retry = models.IntegerField(
                            verbose_name=_("Task Retries"), 
                            default=0)

    duration = models.IntegerField(
                            verbose_name=_("Run duration"), 
                            default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey(
        'content_type', 'object_id', for_concrete_model=False
    )

    def __str__(self):
        return f"{self.task.name} ({self.state})"

    class Meta:
        get_latest_by = 'created'
        ordering = ['-created']


