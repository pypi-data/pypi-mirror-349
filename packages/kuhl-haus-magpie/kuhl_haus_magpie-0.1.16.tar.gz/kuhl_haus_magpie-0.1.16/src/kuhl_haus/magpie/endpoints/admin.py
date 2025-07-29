from django.contrib import admin
from unfold.admin import ModelAdmin

from kuhl_haus.magpie.endpoints.models import (
    EndpointModel,
    DnsResolver,
    DnsResolverList,
    CarbonClientConfig,
    ScriptConfig
)
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget

from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass


@admin.register(CarbonClientConfig)
class CarbonClientConfigAdmin(ModelAdmin):
    list_display = ('name', 'server_ip', 'pickle_port')
    search_fields = ('name', 'server_ip', 'pickle_port')


@admin.register(ScriptConfig)
class ScriptConfigAdmin(ModelAdmin):
    list_display = ('name', 'application_name', 'log_level', 'namespace_root', 'metric_namespace', 'delay', 'count')
    list_filter = ('application_name', 'log_level', 'namespace_root', 'metric_namespace', 'delay', 'count')
    search_fields = ('name', 'application_name', 'namespace_root', 'metric_namespace')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'application_name',),
        }),
        ('Logging Parameters', {
            'fields': ('log_level',),
        }),
        ('Metrics Parameters', {
            'fields': ('namespace_root', 'metric_namespace',),
        }),
        ('Runtime Parameters', {
            'fields': ('delay', 'count'),
        }),
    )


@admin.register(DnsResolver)
class DnsResolverAdmin(ModelAdmin):
    list_display = ('name', 'ip_address')
    search_fields = ('name', 'ip_address')


@admin.register(DnsResolverList)
class DnsResolverListAdmin(ModelAdmin):
    filter_horizontal = ('resolvers',)


@admin.register(EndpointModel)
class EndpointModelAdmin(ModelAdmin):
    list_display = ('mnemonic', 'hostname', 'ignore', 'tls_check', 'dns_check', 'health_check', 'response_format', 'dns_resolver_list')
    list_filter = ('ignore', 'tls_check', 'dns_check', 'health_check', 'response_format', 'dns_resolver_list')
    search_fields = ('mnemonic', 'hostname')
    fieldsets = (
        ('Basic Information', {
            'fields': ('mnemonic', 'hostname',)
        }),
        ('Checks', {
            'fields': ('ignore', 'tls_check', 'dns_check', 'health_check',)
        }),
        ('Health Check Configuration', {
            'fields': (
                'scheme', 'port', 'path', 'verb', 'query', 'fragment'
            )
        }),
        ('Post Parameters', {
            'fields': ('body',),
        }),
        ('Response Settings', {
            'fields': ('healthy_status_code', 'response_format')
        }),
        ('JSON Response Settings', {
            'fields': ('status_key', 'healthy_status', 'version_key')
        }),
        ('Timeout Settings', {
            'fields': ('connect_timeout', 'read_timeout')
        }),
        ('Additional Settings', {
            'fields': ('dns_resolver_list',)
        }),
    )
