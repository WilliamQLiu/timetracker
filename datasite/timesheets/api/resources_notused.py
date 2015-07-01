""" tastypie API """
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication
from tastypie.serializers import Serializer
from tastypie import fields  # For ForeignKey relationships
from timesheets.models import Program, Time, CostCode

"""
    curl --user "test_user":"123" "http://127.0.0.1:8000/api/v1/program/?format=json"
"""

class TimeResource(ModelResource):
    class Meta:
        queryset = Time.objects.all()
        allowed_methods = ['get']
        authentication = BasicAuthentication()

    def get_object_list(self, request):
        """ returns a list of Time objects """
        return super(TimeResource, self).get_object_list(request)


class CostCodeResource(ModelResource):
    class Meta:
        queryset = CostCode.objects.all()
        allowed_methods = ['get']
        authentication = BasicAuthentication()

    def get_object_list(self, request):
        """ returns a list of Time objects """
        return super(CostCodeResource, self).get_object_list(request)


class ProgramResource(ModelResource):
    #The relationship
    time_key = fields.ForeignKey(TimeResource, 'time')
    costcode_key = fields.ForeignKey(CostCodeResource, 'program_select')

    class Meta:
        queryset = Program.objects.all()
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        excludes =['notes']
        #resource_name = 'date_select'
        serializer = Serializer()

    def get_object_list(self, request):
        """ returns a list of Program objects """
        #test = Time.objects.select_related().all().filter(user=request.user)

        #return super(ProgramResource, self).get_object_list(request)
        #times = Time.objects.select_related().all().filter(user_id=request.user)
        return super(ProgramResource, self).get_object_list(request)

    def dehydrate(self, bundle):
        """ Let's us set additional items """
        bundle.data['test_date'] = 'ABC'
        #bundle.data['my_time'] = Time.objects.select_related().filter(time_id=times)
        return bundle
