from django.contrib import admin

from .models import Risk, RiskTextField, RiskNumberField, RiskDateTimeField

class RiskTextFieldInline(admin.TabularInline):
    model = RiskTextField

class RiskNumberFieldInline(admin.TabularInline):
    model = RiskNumberField

class RiskDateTimeFieldInline(admin.TabularInline):
    model = RiskDateTimeField

class RiskAdmin(admin.ModelAdmin):
    inlines = [
        RiskTextFieldInline,
        RiskNumberFieldInline,
        RiskDateTimeFieldInline
    ]

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        if obj:
            return extra - obj.binarytree_set.count()
        return extra

admin.site.register(Risk, RiskAdmin)
