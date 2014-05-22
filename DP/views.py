from django.views import generic
from django.shortcuts import HttpResponseRedirect, render_to_response
from django.contrib.auth.models import User
from DP.models import Project, Site, Location, ObjectOfStudy, CurrentProject
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from DP.forms import CreateProjectForm
from DP.forms import CreateLocationForm
from DP.forms import CreateSiteForm
from DP.forms import CreateOOSForm, OOSUpdateForm
from DP.forms import MeasurementForm
from DP.forms import InputForm, IntUpdateForm, BoolUpdateForm, DeciUpdateForm, FloatUpdateForm, CharUpdateForm

from DP.models import IntField
from DP.models import BoolField
from DP.models import DeciField
from DP.models import FloatField
from DP.models import CharField

from DP.models import IntMeasurement
from DP.models import BoolMeasurement
from DP.models import DeciMeasurement
from DP.models import FloatMeasurement
from DP.models import CharMeasurement

from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy


class MainView(generic.TemplateView):
    template_name = "DP/main.html"


class ProjectDashboard(generic.TemplateView):
    template_name = "DP/projectdashboard.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectDashboard, self).get_context_data(**kwargs)
        context['project'] = Project.objects.filter(pk=kwargs['project_pk'])[0]

        s = User.objects.filter(pk=self.request.user.pk)[0]
        current = CurrentProject.objects.filter(user=s)
        if not current.exists():
            new = CurrentProject(user=s, project=context['project'])
            new.save()
        else:
            current = current[0]
            current.project = context['project']
            current.save()
        return context


class CreateProject(generic.CreateView):
    template_name = "DP/createproject.html"
    model = Project
    form_class = CreateProjectForm
    success_url = '/'

    def form_valid(self, form, **kwargs):
        project = form.save(commit=False)
        u = User.objects.filter(pk=self.request.user.pk)[0]
        project.investigator = u # use your own profile here
        project.save()
        return HttpResponseRedirect(self.success_url)


class CreateSite(CreateView):
    template_name = "DP/createsite.html"
    model = Site
    form_class = CreateSiteForm

    def form_valid(self, form, **kwargs):
        site = form.save(commit=False)
        s = User.objects.filter(pk=self.request.user.pk)[0]
        c = CurrentProject.objects.filter(user=s)[0]
        site.project = c.project # use your own profile here
        site.save()
        CreateSite.success_url = c.get_absolute_url()
        return HttpResponseRedirect(self.success_url)


class CreateLocation(CreateView):
    template_name = "DP/createlocation.html"
    model = Location
    form_class = CreateLocationForm

    def form_valid(self, form, **kwargs):
        location = form.save(commit=False)
        l = User.objects.filter(pk=self.request.user.pk)[0]
        c = CurrentProject.objects.filter(user=l)[0]
        location.project = c.project # use your own profile here
        location.save()
        CreateLocation.success_url = c.get_absolute_url()
        return HttpResponseRedirect(self.success_url)


class CreateOOS(CreateView):
    template_name = "DP/createoos.html"
    model = ObjectOfStudy
    form_class = CreateOOSForm

    def form_valid(self, form, **kwargs):
        oos = form.save(commit=False)
        p = User.objects.filter(pk=self.request.user.pk)[0]
        c = CurrentProject.objects.filter(user=p)[0]
        oos.createdby = p # use your own profile here
        oos.save()
        oos.project.add(c.project)
        oos.save()
        CreateOOS.success_url = c.get_absolute_url()
        return HttpResponseRedirect(self.success_url)


class CreateMeasure(FormView):
    template_name = "DP/createmeasurement.html"
    form_class = MeasurementForm

    def form_valid(self, form):
        current = CurrentProject.objects.filter(user=self.request.user)[0]

        m = User.objects.filter(pk=self.request.user.pk)[0]
        c = CurrentProject.objects.filter(user=m)[0]
        CreateMeasure.success_url = c.get_absolute_url()

        if form.cleaned_data['measure_type'] == '1':
            new_field = IntField(name=form.cleaned_data['name'],
                                 description=form.cleaned_data['description'],
                                 nullable=form.cleaned_data['nullable'],
                                 default=form.cleaned_data['default'],
                                 oos=form.cleaned_data['oos'],
                                 project=current.project
                                 )
            new_field.save()
        elif form.cleaned_data['measure_type'] == '2':
            new_field = BoolField(name=form.cleaned_data['name'],
                                  description=form.cleaned_data['description'],
                                  nullable=form.cleaned_data['nullable'],
                                  default=form.cleaned_data['default'],
                                  oos=form.cleaned_data['oos'],
                                  project=current.project
                                  )
            new_field.save()
        elif form.cleaned_data['measure_type'] == '3':
            new_field = DeciField(name=form.cleaned_data['name'],
                                  description=form.cleaned_data['description'],
                                  nullable=form.cleaned_data['nullable'],
                                  default=form.cleaned_data['default'],
                                  oos=form.cleaned_data['oos'],
                                  project=current.project
                                  )
            new_field.save()
        elif form.cleaned_data['measure_type'] == '4':
            new_field = FloatField(name=form.cleaned_data['name'],
                                   description=form.cleaned_data['description'],
                                   nullable=form.cleaned_data['nullable'],
                                   default=form.cleaned_data['default'],
                                   oos=form.cleaned_data['oos'],
                                   project=current.project
                                   )
            new_field.save()
        elif form.cleaned_data['measure_type'] == '5':
            new_field = CharField(name=form.cleaned_data['name'],
                                  description=form.cleaned_data['description'],
                                  nullable=form.cleaned_data['nullable'],
                                  default=form.cleaned_data['default'],
                                  oos=form.cleaned_data['oos'],
                                  project=current.project
                                  )
            new_field.save()

        return HttpResponseRedirect(self.success_url)


class ViewData(CreateView):
    pass


class EnterData(FormView):
    template_name = "DP/enterdata.html"
    form_class = InputForm
    success_url = '/'

    def get_fields(self):
        u = User.objects.filter(pk=self.request.user.pk)[0]
        p = CurrentProject.objects.filter(user=u)[0]
        fields = []
        field_types = [IntField, BoolField, DeciField, FloatField, CharField]
        for f in field_types:
            f = f.objects.filter(project=p.project)
            fields += f[0:]
        self.fields = fields
        return fields

    def get_context_data(self, **kwargs):
        context = super(EnterData, self).get_context_data(**kwargs)
        if self.fields:
            context['fields'] = self.fields
        else:
            context['fields'] = self.get_fields()
        return context


    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
            'fields': self.get_fields(),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        print(form.cleaned_data)
        if form.cleaned_data['measure_type'] == '1':
            new_field = IntMeasurement(measurement_id=form.cleaned_data['measurement_id'],
                                       value=form.cleaned_data['value'],
                                       nullable=form.cleaned_data['nullable'],
                                       date=form.cleaned_data['date'],
                                       )
            new_field.save()
        elif form.cleaned_data['measure_type'] == '2':
            new_field = BoolMeasurement(measurement_id=form.cleaned_data['measurement_id'],
                                        value=form.cleaned_data['value'],
                                        nullable=form.cleaned_data['nullable'],
                                        date=form.cleaned_data['date'],
                                        )
            new_field.save()
        elif form.cleaned_data['measure_type'] == '2':
            new_field = DeciMeasurement(measurement_id=form.cleaned_data['measurement_id'],
                                        value=form.cleaned_data['value'],
                                        nullable=form.cleaned_data['nullable'],
                                        date=form.cleaned_data['date'],
                                        )
            new_field.save()
        elif form.cleaned_data['measure_type'] == '2':
            new_field = FloatMeasurement(measurement_id=form.cleaned_data['measurement_id'],
                                         value=form.cleaned_data['value'],
                                         nullable=form.cleaned_data['nullable'],
                                         date=form.cleaned_data['date'],
                                         )
            new_field.save()
        elif form.cleaned_data['measure_type'] == '2':
            new_field = CharMeasurement(measurement_id=form.cleaned_data['measurement_id'],
                                        value=form.cleaned_data['value'],
                                        nullable=form.cleaned_data['nullable'],
                                        date=form.cleaned_data['date'],
                                        )
            new_field.save()

        return HttpResponseRedirect(self.success_url)


class Layout_Test(generic.TemplateView):
    template_name = "DP/layout_test.html"


class EditProject(generic.TemplateView):
    template_name = "DP/editproject.html"


class ManageFields(generic.TemplateView):
    template_name = "DP/managefields.html"

    def get_fields(self):
        u = User.objects.filter(pk=self.request.user.pk)[0]
        p = CurrentProject.objects.filter(user=u)[0].project
        fields = []
        field_types = [IntField, BoolField, DeciField, FloatField, CharField]
        for f in field_types:
            f = f.objects.filter(project=p)
            fields += f[0:]
        self.fields = fields
        return fields

    def get_oosfields(self):
        u = User.objects.filter(pk=self.request.user.pk)[0]
        p = CurrentProject.objects.filter(user=u)[0].project
        oos_fields = []
        oos_field = [ObjectOfStudy]
        for o in oos_field:
            o = o.objects.filter(project=p)
            oos_fields += o[0:]
        self.oos_fields = oos_fields
        return oos_fields

    def get_context_data(self, **kwargs):
        context = super(ManageFields, self).get_context_data(**kwargs)
        context['fields'] = self.get_fields()
        context['oos_fields'] = self.get_oosfields()
        return context


class FieldUpdate2(generic.UpdateView):
    template_name = "DP/fieldupdate.html"
    success_url = '/projectdashboard/'

    def get_object(self):
        lookup = {'1': IntField,
                  '2': BoolField,
                  '3': DeciField,
                  '4': FloatField,
                  '5': CharField}
        lookup2 = {'1': IntUpdateForm,
                   '2': BoolUpdateForm,
                   '3': DeciUpdateForm,
                   '4': FloatUpdateForm,
                   '5': CharUpdateForm}
        FieldUpdate2.form_class = lookup2[self.kwargs['f_type']]
        FieldUpdate2.model = lookup[self.kwargs['f_type']]

        project = Project.objects.filter(pk=int(self.kwargs['project_pk']))[0]
        p = CurrentProject.objects.filter(user=self.request.user, project=project)[0]
        FieldUpdate2.success_url = p.get_absolute_url()
        return self.model.objects.get(project=project, pk=self.kwargs['field_pk'])

    def form_valid(self, form):
        update = self.get_object()
        update.name = form.cleaned_data['name']
        update.nullable = form.cleaned_data['nullable']
        update.default = form.cleaned_data['default']
        update.oos = form.cleaned_data['oos']
        update.description = form.cleaned_data['description']
        update.save()
        return HttpResponseRedirect(self.success_url)


class ViewField(DetailView):
    template_name = "DP/viewfield.html"
    success_url = '/projectdashboard/'
    context_object_name = 'field'
    ### Finish the viewfield page, and this with a queryset.

    def get_object(self):
        lookup = {'1': IntField,
                  '2': BoolField,
                  '3': DeciField,
                  '4': FloatField,
                  '5': CharField}
        ViewField.model = lookup[self.kwargs['f_type']]

        project = Project.objects.filter(pk=int(self.kwargs['project_pk']))[0]
        p = CurrentProject.objects.filter(user=self.request.user, project=project)[0]
        ViewField.success_url = p.get_absolute_url()
        return self.model.objects.get(project=project, pk=self.kwargs['field_pk'])


class DeleteFieldObjects(DeleteView):
    template_name = "DP/fielddelete.html"
    success_url = '/projectdashboard/'

    def get_queryset(self):
        return ObjectOfStudy.objects.filter(user=self.request.user)
    ### This is an example form the GPA site, so that we can look further into writing the correct queryset.

    def get_object(self):
        lookup = {'1': IntField,
                  '2': BoolField,
                  '3': DeciField,
                  '4': FloatField,
                  '5': CharField}
        lookup2 = {'1': IntUpdateForm,
                   '2': BoolUpdateForm,
                   '3': DeciUpdateForm,
                   '4': FloatUpdateForm,
                   '5': CharUpdateForm}
        DeleteFieldObjects.form_class = lookup2[self.kwargs['f_type']]
        DeleteFieldObjects.model = lookup[self.kwargs['f_type']]

        project = Project.objects.filter(pk=int(self.kwargs['project_pk']))[0]
        p = CurrentProject.objects.filter(user=self.request.user, project=project)[0]
        DeleteFieldObjects.success_url = p.get_absolute_url()
        return self.model.objects.get(project=project, pk=self.kwargs['field_pk'])


class OOSUpdate(generic.UpdateView):
    model = ObjectOfStudy
    fields = ['name']
    template_name = "DP/oosupdate.html"
    form_class = OOSUpdateForm
    # success_url = '/projectdashboard/'

    def get_object(self):
        project = Project.objects.filter(pk=int(self.kwargs['project_pk']))[0]
        p = CurrentProject.objects.filter(user=self.request.user, project=project)[0]
        OOSUpdate.success_url = p.get_absolute_url()
        return self.model.objects.get(project=project, pk=self.kwargs['oos_fields_pk'])

    def form_valid(self, form):
        update = self.get_object()
        update.name = form.cleaned_data['name']
        update.description = form.cleaned_data['description']
        update.save()
        return HttpResponseRedirect(self.success_url)


class DeleteOOSObjects(DeleteView):
    model = ObjectOfStudy
    template_name = "DP/oosdelete.html"
    # success_url = '/projectdashboard/'

    def get_queryset(self):
        return ObjectOfStudy.objects.filter(user=self.request.user)
    ### This is an example form the GPA site, so that we can look further into writing the correct queryset.

    def get_object(self):
        project = Project.objects.filter(pk=int(self.kwargs['project_pk']))[0]
        p = CurrentProject.objects.filter(user=self.request.user, project=project)[0]
        DeleteOOSObjects.success_url = p.get_absolute_url()
        return self.model.objects.get(project=project, pk=self.kwargs['oos_fields_pk'])


class OOSView(DetailView):
    model = ObjectOfStudy
    template_name = "DP/oosview.html"
    # success_url = '/projectdashboard/'
    context_object_name = 'oos'
    ### Finish the viewfield page, and this with a queryset.

    def get_object(self):
        project = Project.objects.filter(pk=int(self.kwargs['project_pk']))[0]
        p = CurrentProject.objects.filter(user=self.request.user, project=project)[0]
        OOSView.success_url = p.get_absolute_url()
        return self.model.objects.get(project=project, pk=self.kwargs['oos_fields_pk'])





