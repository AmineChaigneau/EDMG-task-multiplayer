from django.contrib import admin
from .models import Round, Trial, Calibration, Form
from .actions import export_csv

class RoundAdmin(admin.ModelAdmin):
    actions = [export_csv]

class TrialAdmin(admin.ModelAdmin):
    actions = [export_csv]

class CalibrationAdmin(admin.ModelAdmin):
    actions = [export_csv]

class FormAdmin(admin.ModelAdmin):
    actions = [export_csv]

admin.site.register(Round, RoundAdmin)
admin.site.register(Trial, TrialAdmin)
admin.site.register(Calibration, CalibrationAdmin)
admin.site.register(Form, FormAdmin)
