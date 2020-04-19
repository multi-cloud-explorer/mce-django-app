from django.db import models


class Provider(models.TextChoices):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    VMWARE = "vmware"

class EventChangeType(models.TextChoices):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class TaskState(models.TextChoices):
    UNKNOW    = 'unknow'
    QUEUED    = 'queued'
    FINISHED  = 'finished'
    FAILED    = 'failed'
    STARTED   = 'started'
    DEFERRED  = 'deferred'
    SCHEDULED = 'scheduled'
