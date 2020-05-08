from rest_framework.reverse import reverse

"""
/mce/api/v1/common/company/     mce_django_app.api.common.views.CompanyiewSet   common:company-list
/mce/api/v1/common/company/<pk>/        mce_django_app.api.common.views.CompanyiewSet   common:company-detail
/mce/api/v1/common/company/<pk>\.<format>/      mce_django_app.api.common.views.CompanyiewSet   common:company-detail
/mce/api/v1/common/company\.<format>/   mce_django_app.api.common.views.CompanyiewSet   common:company-list
"""