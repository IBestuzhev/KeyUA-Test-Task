from django.conf.urls.defaults import patterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^%s$'%settings.LOGIN_URL[1:],'django.contrib.auth.views.login',
            {'template_name':'Login.html'}),
    (r'^profile/logout/$','django.contrib.auth.views.logout',
            {'next_page':'/', 'redirect_field_name':'next'},'logout_view'),
    (r'(?P<path>.*[.](?:css|js|html|jpg|jpeg|png|gif))',
            'django.views.static.serve',
            {'document_root': 'c:\\work\\KeyUA\\keyuatest\\static'})
)

urlpatterns += patterns('profileapp.views',
    (r'^$', 'list_profile',None,'list_profile'),
    (r'^(?P<user>[a-zA-Z0-9]+)/$','show_profile'),
    (r'^edit/(?P<user>[a-zA-Z0-9]+)/$','edit_profile',None,'edit_profile')
    # Example:
    # (r'^keyuatest/', include('keyuatest.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
