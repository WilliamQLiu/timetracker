from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User


class Department(models.Model):
    """ List Types of Departments """
    name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.name)

    def natural_key(self):
        return (self.name)


class JobType(models.Model):
    """ Whether employees are full time, part time, contract, internship """
    status = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.status)

    def natural_key(self):
        return (self.status)


class UserProfile(models.Model):
    """ Extending the User Model """
    user = models.OneToOneField(User)
    # one user can only have one user profile (and vice versa)
    department = models.ForeignKey(Department, null=True, blank=True)
    status = models.ForeignKey(JobType, null=True, blank=True)
    start_date = models.DateField(default='2000-1-1', null=False, blank=True)
    end_date = models.DateField(default='2050-1-1', null=False, blank=True)
    stillhere = models.BooleanField(default=True, blank=True)
    salary = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.user)

    def natural_key(self):
        return (self.user)


class TimeManager(models.Manager):
    def get_by_natural_key(self, date_select):
        return self.get(date_select=date_select)


class Time(models.Model):
    """ Enter time """
    # A primary key 'id' is automatically created
    # id = models.AutoField(primary_key=True)
    objects = TimeManager()

    user = models.ForeignKey(User)
    date_select = models.DateField()
    timestamp_created = models.DateTimeField(auto_now=False,  # Update now
                                             auto_now_add=True  # When create
                                             )
    timestamp_updated = models.DateTimeField(auto_now=True,  # Update now
                                             auto_now_add=False  # When create
                                             )

    def __unicode__(self):
        return smart_unicode(self.date_select)  # Name is the Date

    class Meta:
        ordering = ['-date_select']  # Automatically order by latest first

    def natural_key(self):
        return (self.date_select)  # Natural Keys need lists even if one item


class CostCodeManager(models.Manager):
    def get_by_natural_key(self, program_name):
        return self.get(program_name=program_name)

    #def get_active(self):
    #    return self.filter(active = 1)


class CostCode(models.Model):
    """ Select list of Programs and Cost Codes """

    objects = CostCodeManager()

    program_name = models.TextField()
    cost_code = models.TextField()
    active = models.BooleanField(default=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.program_name)

    def natural_key(self):
        return (self.program_name)


class ProgramManager(models.Manager):
    users = models.ManyToManyField(User, through='Job')

    def get_by_natural_key(self, program_select, hours_spent,
                           minutes_spent, notes):
        return self.get(program_select=program_select,
                        hours_spent=hours_spent,
                        minutes_spent=minutes_spent,
                        notes=notes)


class Program(models.Model):
    """ Enter time spent on program """
    objects = ProgramManager()
    time = models.ForeignKey(Time)  # FK is a many-to-one relationship
    program_select = models.ForeignKey(CostCode)
    hours_spent = models.IntegerField(null=True, blank=True)  # Time Spent
    minutes_spent = models.IntegerField(null=True, blank=True)  # Time Spent
    notes = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return smart_unicode(self.program_select)

    class Meta:
        ordering = ['time']  # Automatically order by latest first

    def natural_key(self):
        return (self.program_select, self.hours_spent,
                self.minutes_spent, self.notes)

