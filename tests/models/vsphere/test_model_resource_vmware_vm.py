# import pytest
#
# from django.core.exceptions import ValidationError
#
# from mce_django_app.models import vsphere as models
#
# CURRENT_MODEL = models.ResourceVMwareVM
#
# def test_create_success(
#         mce_app_company,
#         mce_app_provider_vmware,
#         mce_app_resource_type_vsphere_vm,
#         mce_app_vsphere_datacenter):
#     """Simple create"""
#
#     obj = CURRENT_MODEL.objects.create(
#         name="myvm",
#         resource_id="group-d1/datacenter-dc0/folder-1/vm-myvm",
#         resource_type=mce_app_resource_type_vsphere_vm,
#         company=mce_app_company,
#         provider=mce_app_provider_vmware,
#         datacenter=mce_app_vsphere_datacenter
#     )
#
#     assert obj.slug == "group-d1-datacenter-dc0-folder-1-vm-myvm"
#
# def test_error_duplicate(
#         mce_app_company,
#         mce_app_provider_vmware,
#         mce_app_resource_type_vsphere_vm,
#         mce_app_vsphere_datacenter):
#     """check error if duplicate object"""
#
#     CURRENT_MODEL.objects.create(
#         name="myvm",
#         resource_id="group-d1/datacenter-dc0/folder-1/vm-myvm",
#         resource_type=mce_app_resource_type_vsphere_vm,
#         company=mce_app_company,
#         provider=mce_app_provider_vmware,
#         datacenter=mce_app_vsphere_datacenter
#     )
#
#     with pytest.raises(ValidationError) as excinfo:
#         CURRENT_MODEL.objects.create(
#             name="myvm",
#             resource_id="group-d1/datacenter-dc0/folder-1/vm-myvm",
#             resource_type=mce_app_resource_type_vsphere_vm,
#             company=mce_app_company,
#             provider=mce_app_provider_vmware,
#             datacenter=mce_app_vsphere_datacenter
#         )
#     assert excinfo.value.message_dict == {
#         'resource_id': ['Resource with this Resource id already exists.'],
#     }
#
# def test_error_max_length(
#         mce_app_company,
#         mce_app_provider_vmware,
#         mce_app_resource_type_vsphere_vm,
#         mce_app_vsphere_datacenter):
#     """Test max_length constraints"""
#
#     with pytest.raises(ValidationError) as excinfo:
#         CURRENT_MODEL.objects.create(
#             name="x" * 256,
#             resource_id="x" * 1025,
#             resource_type=mce_app_resource_type_vsphere_vm,
#             company=mce_app_company,
#             provider=mce_app_provider_vmware,
#             datacenter=mce_app_vsphere_datacenter
#         )
#     assert excinfo.value.message_dict == {
#         'name': ['Ensure this value has at most 255 characters (it has 256).'],
#         'resource_id': ['Ensure this value has at most 1024 characters (it has 1025).'],
#     }
#
# def test_error_null_and_blank_value(
#         mce_app_company,
#         mce_app_provider_vmware,
#         mce_app_resource_type_vsphere_vm,
#         mce_app_vsphere_datacenter):
#     """test null and blank value"""
#
#     with pytest.raises(ValidationError) as excinfo:
#         CURRENT_MODEL.objects.create(
#             name="",
#             resource_id="",
#             resource_type=mce_app_resource_type_vsphere_vm,
#             company=mce_app_company,
#             provider=mce_app_provider_vmware,
#             datacenter=mce_app_vsphere_datacenter
#         )
#
#     assert excinfo.value.message_dict == {
#         'name': ['This field cannot be blank.'],
#         'resource_id': ['This field cannot be blank.'],
#     }
#
#     with pytest.raises(ValidationError) as excinfo:
#         CURRENT_MODEL.objects.create()
#     assert excinfo.value.message_dict == {
#         'name': ['This field cannot be blank.'],
#         'resource_id': ['This field cannot be blank.'],
#         'resource_type': ['This field cannot be null.'],
#         'company': ['This field cannot be null.'],
#         'provider': ['This field cannot be null.'],
#         'datacenter': ['This field cannot be null.'],
#     }
#
