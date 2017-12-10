from django.contrib import admin

from .models import Risk, RiskTextField, RiskNumberField, RiskDateTimeField

class RiskTextFieldInline(admin.TabularInline):
    model = RiskTextField
    extra = 0

class RiskNumberFieldInline(admin.TabularInline):
    model = RiskNumberField
    extra = 0

class RiskDateTimeFieldInline(admin.TabularInline):
    model = RiskDateTimeField
    extra = 0

class RiskAdmin(admin.ModelAdmin):
    inlines = [
        RiskTextFieldInline,
        RiskNumberFieldInline,
        RiskDateTimeFieldInline
    ]

admin.site.register(Risk, RiskAdmin)
