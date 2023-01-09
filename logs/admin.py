from django.contrib import admin
from django.template.response import TemplateResponse
from logs.models import concat_log, keywords_log
from coutoEditor.global_variable import BASE_DIR
from .helper import get_latest_logs

@admin.register(concat_log)
class concat_logAdmin(admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        text = get_latest_logs(BASE_DIR + '/logs/concat_logs/concat.txt')
        html = "<br>".join(text.split('\n'))
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            html=html,
        )
        return TemplateResponse(request, "logs.html", context)

@admin.register(keywords_log)
class keywords_logAdmin(admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        text = get_latest_logs(BASE_DIR + '/logs/keywords_log/keywords.txt')
        text = text[1:len(text) - 1]
        html = "<br>".join(text.split(','))
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            html=html,
        )
        return TemplateResponse(request, "logs2.html", context)