from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
# auth_views is a workaround for django-registration Django 1.6 issues
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
#from django.conf.urls.static import static

import timesheets.views  # For Class-Based Views
#from timesheets.models import Program

# To fix unexpected keyword argument
#from django.conf.urls.defaults import *
#urlpatterns = auth_views.urlpatterns

admin.autodiscover()

### Start Django REST Framework API
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'data', timesheets.views.DataViewSet)
#router.register(r'users', timesheets.views.UserViewSet)
#router.register(r'groups', timesheets.views.GroupViewSet)
#router.register(r'time', timesheets.views.TimeViewSet)
#router.register(r'costcode', timesheets.views.CostCodeViewSet)
#router.register(r'userprofile', timesheets.views.UserProfileViewSet)
### End Django REST Framework API


urlpatterns = patterns('',

    #Class-Based Views Below
    url(r"^timesheet$", timesheets.views.ProgramListView.as_view(),
        name="timesheet"),
    url(r'^update/(?P<pk>\d+)/$', timesheets.views.ProgramUpdateView.as_view(),
        name='program-update',),
    url(r'^delete/(?P<pk>\d+)/$', timesheets.views.ProgramDeleteView.as_view(),
        name='program-delete',),
    url(r'^program_create$', timesheets.views.ProgramCreateView.as_view(),
        name='program-create',),  # CBV
    #url(r'^program_create$', timesheets.views.programcreate,
    #    name='program-create',),  # FBV

    # Blank Page
    url(r'^$', 'timesheets.views.blank', name='blank'),

    # Data Viz Pages
    #url(r'^datavis$', 'datavis.views.datavis', name='datavis'),

    # Encrypt Page
    url(r'^encrypt$', 'timesheets.views.encrypt', name='encrypt'),

    # Begin django-registration pages, e.g. login and logout
    url(r'^password/change/$',
        auth_views.password_change,
        name='password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        name='password_reset'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),

    #and now add the registration urls
    url(r'', include('registration.backends.default.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    # End django-registration

    # Admin Page
    url(r'^admin/', include(admin.site.urls)),

    # Reports Page
    url(r'^report$', 'timesheets.views.report', name='report'),

    # Download CSV data
    url(r'^downloadsummary$', 'timesheets.views.download_summary',
        name='download-summary'),

    # Get Raw SQL data
    url(r'^downloadraw$', 'timesheets.views.download_raw',
        name='download-raw'),

    # Django Rest Framework (Class Based View)
    #url(r'^stuff/$', timesheets.views.DataList.as_view()),
    #url(r'^stuff/(?P<pk>[0-9]+)/$', timesheets.views.DataDetail.as_view()),

    # For Django REST Framework API
    # Additionally, we include login URLS for the browseable API
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),

    url(r'^', include(router.urls)),

)

#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve Static Media
if settings.DEBUG:
    urlpatterns += patterns('',
                            #url(r'^__debug__/', include(debug_toolbar.urls)),
                            (r'^media/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}),
                            )
