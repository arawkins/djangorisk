from django.db import models

class Risk(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'fields': []
        }

        for field in self.textfields.all():
            data['fields'].append(field.get_json())

        for field in self.numberfields.all():
            data['fields'].append(field.get_json())

        for field in self.datetimefields.all():
            data['fields'].append(field.get_json())

        return data

class RiskField(models.Model):
    TEXT = 'text'
    NUMBER = 'number'
    DATETIME = 'datetime'

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_json(self):
        return {
            'id'  : self.id,
            'name': self.name,
        }

    class Meta:
        abstract = True

class RiskTextField(RiskField):
    value = models.TextField(blank=True, null=True)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='textfields')

    def get_json(self):
        data = super(RiskTextField, self).get_json()
        data['type'] = RiskField.TEXT
        return data

class RiskNumberField(RiskField):
    value = models.DecimalField(blank=True, null=True, max_digits=24, decimal_places=2)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='numberfields')

    def get_json(self):
        data = super(RiskNumberField, self).get_json()
        data['type'] = RiskField.NUMBER
        return data

class RiskDateTimeField(RiskField):
    value = models.DateTimeField(blank=True, null=True)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='datetimefields')

    def get_json(self):
        data = super(RiskDateTimeField, self).get_json()
        data['type'] = RiskField.DATETIME
        return data
