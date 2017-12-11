from django.db import models

# make separate riskdata, and relate field models to that
# make basic Risk have just a normal meta field relation to denote structure

class Risk(models.Model):
    """ A class to model risks.

        Has an unlimited number of reverse foreign key
        relationships with RiskFields, which define
        what data can be stored in this risk.
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_json(self):
        """ Returns a json representation of this risk. """

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

        for field in self.enumfields.all():
            data['fields'].append(field.get_json())

        return data

class RiskField(models.Model):
    """ An abstract class to base our different risk fields off of.

    Includes constants, a common name field, and a boilerplate
    get_json method that will be overridden by child classes.
    ForeignKey relationships to the Risk are defined in the child
    classes.
    """

    # Type constants
    TEXT = 'text'
    NUMBER = 'number'
    DATETIME = 'datetime'
    ENUM = 'enum'

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_json(self):
        """ Returns a JSON representation of this field """

        return {
            'id'  : self.id,
            'name': self.name
        }

    class Meta:
        abstract = True

class RiskTextField(RiskField):
    """ A field to hold text data on risks """
    value = models.TextField(blank=True, null=True)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='textfields')

    def get_json(self):
        data = super(RiskTextField, self).get_json()
        data['type'] = RiskField.TEXT
        return data

class RiskNumberField(RiskField):
    """ A field to hold numerical values on a risk. """
    value = models.DecimalField(blank=True, null=True, max_digits=24, decimal_places=2)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='numberfields')

    def get_json(self):
        data = super(RiskNumberField, self).get_json()
        data['type'] = RiskField.NUMBER
        return data

class RiskDateTimeField(RiskField):
    """ A field to hold Datetime information on risks """
    value = models.DateTimeField(blank=True, null=True)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='datetimefields')

    def get_json(self):
        data = super(RiskDateTimeField, self).get_json()
        data['type'] = RiskField.DATETIME
        return data


class RiskEnumField(RiskField):
    """ A field to hold text data on a risk.

    Has a defined set of possible values,
    stored as a pipe delimited string.
    """

    value = models.CharField(blank=True, null=True, max_length=128)
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='enumfields')

    # possible_values should be a pipe delimted string of possible values for this field
    possible_values = models.TextField(blank=True, null=True)

    def get_json(self):
        data = super(RiskEnumField, self).get_json()
        data['type'] = RiskField.ENUM
        data['possible_values'] = self.get_list_of_possible_values()
        return data

    def get_list_of_possible_values(self):
        """ Splits the pipe delimited possible_values string into a list """
        return [value.strip() for value in self.possible_values.split('|')]
