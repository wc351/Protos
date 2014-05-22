from django import forms
from DP.models import Project, Site, Location, ObjectOfStudy, IntField
from DP.models import IntField, BoolField, DeciField, CharField, FloatField

MEASURE_CHOICES = [(1, "Integer"), (2, "Boolean"), (3, "Decimal"), (4, "Float"), (5, "Text")]


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('investigator',)


class CreateSiteForm(forms.ModelForm):
    class Meta:
        model = Site
        exclude = ('project',)


class CreateLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ('project',)


class CreateOOSForm(forms.ModelForm):
    class Meta:
        model = ObjectOfStudy
        exclude = ('createdby', 'project')


class OOSUpdateForm(forms.ModelForm):
    class Meta:
        model = ObjectOfStudy
        exclude = ('createdby', 'project')


class IntUpdateForm(forms.ModelForm):
    class Meta:
        model = IntField
        exclude = ('project',)


class BoolUpdateForm(forms.ModelForm):
    class Meta:
        model = BoolField
        exclude = ('project',)


class DeciUpdateForm(forms.ModelForm):
    class Meta:
        model = DeciField
        exclude = ('project',)


class FloatUpdateForm(forms.ModelForm):
    class Meta:
        model = FloatField
        exclude = ('project',)


class CharUpdateForm(forms.ModelForm):
    class Meta:
        model = CharField
        exclude = ('project',)


class MeasurementForm(forms.Form):
    name = forms.CharField()
    oos = forms.ModelChoiceField(queryset=ObjectOfStudy.objects.filter())
    measure_type = forms.ChoiceField(choices=MEASURE_CHOICES, widget=forms.RadioSelect)
    nullable = forms.BooleanField(widget=forms.RadioSelect, initial=True, required=False)
    default = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)


class InputForm(forms.Form):

    oos = forms.ModelChoiceField(queryset=ObjectOfStudy.objects.filter())

    def __init__(self, *args, **kwargs):
        form_fields = kwargs.pop("fields", {})
        super(InputForm, self).__init__(*args, **kwargs)
        for field in form_fields:
            # Create the form field
            if field.__class__.__name__ == 'IntField':
                self.fields[field.name] = forms.IntegerField(required=True, label=field.name)

            elif field.__class__.__name__ == 'BoolField':
                self.fields[field.name] = forms.BooleanField(required=True, label=field.name)

            elif field.__class__.__name__ == 'DeciField':
                self.fields[field.name] = forms.DecimalField(required=True, label=field.name)

            elif field.__class__.__name__ == 'FloatField':
                self.fields[field.name] = forms.FloatField(required=True, label=field.name)

            elif field.__class__.__name__ == 'CharField':
                self.fields[field.name] = forms.CharField(required=True, label=field.name)

    # measure_type = forms.ChoiceField(choices=MEASURE_CHOICES, widget=forms.RadioSelect)
    # site = forms.ModelChoiceField(queryset=Site.objects.filter())
    # location = forms.ModelChoiceField(queryset=Location.objects.filter())