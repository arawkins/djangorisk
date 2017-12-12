from django.db import models

class Risk(models.Model):
    """ A class to model risks.

        Has an unlimited number of reverse foreign key
        relationships with RiskFields, which define
        what data can be stored in this risk.
    """

    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_data(self):
        """ Returns a dictionary representation of this risk.

        Fields that are related to this risk are gathered and
        added to a fields list in the dictionary.
        """

        data = {
            'id': self.id,
            'name': self.name,
            'fields': []
        }

        for field in self.textfields.all():
            data['fields'].append(field.get_data())

        for field in self.numberfields.all():
            data['fields'].append(field.get_data())

        for field in self.datetimefields.all():
            data['fields'].append(field.get_data())

        for field in self.enumfields.all():
            data['fields'].append(field.get_data())

        return data

class RiskField(models.Model):
    """ An abstract base class to base our different risk fields off of.

    Includes constants, common model field, and a boilerplate
    get_data method that will be overridden by child classes.
    Since each child class is responsible for a specific data type,
    ForeignKey relationships to Risks are defined in the child
    class, as are value fields, for holding data.
    """

    # Type constants
    TEXT = 'text'
    NUMBER = 'number'
    DATETIME = 'datetime'
    ENUM = 'enum'

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_data(self):
        """ Returns a dictionary representation of this field

        type and possible_values are defined in child classes
        """

        return {
            'id'  : self.id,
            'name': self.name,
            'type': None,
            'possible_values': None
        }

    class Meta:
        abstract = True

class RiskTextField(RiskField):
    """ A field to hold text data on risks """
    value = models.TextField(blank=True, null=True)
    risk = models.ForeignKey('Risk', on_delete=models.CASCADE, related_name='textfields')

    def get_data(self):
        data = super(RiskTextField, self).get_data()
        data['type'] = RiskField.TEXT
        return data

class RiskNumberField(RiskField):
    """ A field to hold numerical values on a risk. """
    value = models.DecimalField(blank=True, null=True, max_digits=24, decimal_places=2)
    risk = models.ForeignKey('Risk', on_delete=models.CASCADE, related_name='numberfields')

    def get_data(self):
        data = super(RiskNumberField, self).get_data()
        data['type'] = RiskField.NUMBER
        return data

class RiskDateTimeField(RiskField):
    """ A field to hold Datetime information on risks """
    value = models.DateTimeField(blank=True, null=True)
    risk = models.ForeignKey('Risk', on_delete=models.CASCADE, related_name='datetimefields')

    def get_data(self):
        data = super(RiskDateTimeField, self).get_data()
        data['type'] = RiskField.DATETIME
        return data


class RiskEnumField(RiskField):
    """ A field to hold text data on a risk, with a defined set of possible values.

    Possible values are stored as a pipe delimited string.
    """

    value = models.CharField(blank=True, null=True, max_length=128)
    risk = models.ForeignKey('Risk', on_delete=models.CASCADE, related_name='enumfields')
    possible_values = models.TextField(blank=True, null=True)

    def get_data(self):
        data = super(RiskEnumField, self).get_data()
        data['type'] = RiskField.ENUM
        data['possible_values'] = self.get_list_of_possible_values()
        return data

    def get_list_of_possible_values(self):
        """ Returns possible_values string as a list """
        return [value.strip() for value in self.possible_values.split('|')]
