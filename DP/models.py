# from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    investigator = models.ForeignKey(User)
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return "{} - {}".format(self.name,
                                self.investigator)

    def get_absolute_url(self):
        return "/"


class CurrentProject(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "Current Project: {}".format(self.project.name)

    def get_absolute_url(self):
        return "/projectdashboard/{}/".format(self.project.pk)


class Site(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=140)
    description = models.TextField()
    num = models.IntegerField()
    geom = models.GeometryField()
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


class Location(models.Model):
    project = models.ForeignKey(Project)
    collection_area = models.CharField(max_length=140)
    description = models.TextField()
    num = models.IntegerField()
    geom = models.MultiPolygonField()
    objects = models.GeoManager()

    def __unicode__(self):
        return self.collection_area


class ObjectOfStudy(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    createdby = models.ForeignKey(User)
    project = models.ManyToManyField(Project, blank=True)

    def __unicode__(self):
        return "{}".format(self.name)

    # def __unicode__(self):
    #     return "{} - {}".format(self.name,
    #                             self.object_id)


class IntMeasurement(models.Model):
    oos = models.ForeignKey(ObjectOfStudy)
    measurement_id = models.CharField(max_length=50)
    value = models.IntegerField()
    date = models.DateTimeField()
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return "{} - {}".format(self.value,
                                self.date)


class IntField(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    measurements = models.ManyToManyField(IntMeasurement, blank=True)
    nullable = models.BooleanField()
    default = models.IntegerField()
    oos = models.ForeignKey(ObjectOfStudy)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "{} - {}".format(self.project.name,
                                self.name)


class BoolMeasurement(models.Model):
    oos = models.ForeignKey(ObjectOfStudy)
    measurement_id = models.CharField(max_length=50)
    value = models.BooleanField()
    date = models.DateTimeField()
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return "{} - {}".format(self.value,
                                self.date)


class BoolField(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    measurements = models.ManyToManyField(BoolMeasurement, blank=True)
    nullable = models.BooleanField()
    default = models.BooleanField()
    oos = models.ForeignKey(ObjectOfStudy)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "{} - {}".format(self.project.name,
                                self.name)


class DeciMeasurement(models.Model):
    oos = models.ForeignKey(ObjectOfStudy)
    measurement_id = models.CharField(max_length=50)
    value = models.DecimalField(decimal_places=12, max_digits=32)
    date = models.DateTimeField()
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return "{} - {}".format(self.value,
                                self.date)


class DeciField(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    measurements = models.ManyToManyField(DeciMeasurement, blank=True)
    nullable = models.BooleanField()
    default = models.DecimalField(decimal_places=12, max_digits=32)
    oos = models.ForeignKey(ObjectOfStudy)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "{} - {}".format(self.project.name,
                                self.name)


class FloatMeasurement(models.Model):
    oos = models.ForeignKey(ObjectOfStudy)
    measurement_id = models.CharField(max_length=50)
    value = models.FloatField()
    date = models.DateTimeField()
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return "{} - {}".format(self.value,
                                self.date)


class FloatField(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    measurements = models.ManyToManyField(FloatMeasurement, blank=True)
    nullable = models.BooleanField()
    default = models.FloatField()
    oos = models.ForeignKey(ObjectOfStudy)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "{} - {}".format(self.project.name,
                                self.name)


class CharMeasurement(models.Model):
    oos = models.ForeignKey(ObjectOfStudy)
    measurement_id = models.CharField(max_length=50)
    value = models.CharField(max_length=140)
    date = models.DateTimeField()
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return "{} - {}".format(self.value,
                                self.date)


class CharField(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    measurements = models.ManyToManyField(CharMeasurement, blank=True)
    nullable = models.BooleanField()
    default = models.CharField(max_length=140)
    oos = models.ForeignKey(ObjectOfStudy)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "{} - {}".format(self.project.name,
                                self.name)
