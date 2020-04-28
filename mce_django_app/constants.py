from django.db import models

class Provider(models.TextChoices):

    AWS             = "aws"
    AZURE           = "azure"
    GCP             = "gcp"
    VMWARE          = "vmware"
    CROC            = "croc"
    ALIYUN          = "aliyun"
    ORACLE          = "oracle"
    OPENSTACK       = "openstack"
    GANDI           = "gandi"
    OVH             = "ovh"
    CLOUDSTACK      = "cloudstack"
    DIGITALOCEAN    = "digitalocean"

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

class VsphereResourceTypes(models.TextChoices):
    DATACENTER = "vmware/datacenter"
    VIRTUAL_APP = "vmware/virtualapp"
    CLUSTER_COMPUTE_RESOURCE = "vmware/clustercomputeresource"
    FOLDER = "vmware/folder"
    DISTRIBUTED_VIRTUAL_PORTGROUP = "vmware/distributedvirtualportgroup"
    HOST_SYSTEM = "vmware/hostsystem"
    VIRTUAL_MACHINE = "vmware/virtualmachine"
    NETWORK = "vmware/network"
    OPAQUE_NETWORK = "vmware/opaquenetwork"
    RESOURCE_POOL = "vmware/resourcepool"
    COMPUTE_RESOURCE = "vmware/computeresource" # ESX ?
    DATASTORE = "vmware/datastore"
    DISTRIBUTED_VIRTUAL_SWITCH = "vmware/distributedvirtualswitch"
