from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Time, Program, CostCode, Department, JobType
from .models import UserProfile

# Define an inline admin descriptor for UserProfile model
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User Admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# InlineModelAdmin allows to edit models on the same page as a parent model
class ProgramInline(admin.TabularInline):
    model = Program
    #list_display = ('program_select', 'hours_spent', 'minutes_spent', 'notes')
    extra = 4  # By default, allows X extra options
    fk_name = 'time'


class TimeAdmin(admin.ModelAdmin):

    model = Time
    list_select_related = True
    #list_display = ['date_select', ] # 'my_name'
    inlines = [ProgramInline]

    list_display = ['date_select', 'user_name', ]  # 'program__hours_spent',
    #list_filter = ['date_select', 'program__program_select', 'user__username',]
    list_filter = ['date_select', 'user__username',]
    # Add filter by ability on sidebar
    #list_editable = ['date_select',]
    #date_hierarchy = 'date_select'
    #ordering = ('-date_select',) # Sort by reverse date

    #def was_entered_recently(self, obj):
    #    return self.date_select >= timezone.now() - datetime.timedelta(days=14)
    #was_entered_recently.admin_order_field = 'date_select'
    #was_entered_recently.boolean = True
    #was_entered_recently.short_description = 'Entered recently?'

    #def localname(self, obj):
    #    return obj.program.program_select
    #localname.short_description = 'Test'
    #get_program.short_description = 'Program'
    #get_program.admin_order_field = 'program__program_select'

    def user_name(self, obj):
        #return obj.user.first_name + obj.user.last_name
        return obj.user.username

class CostCodeAdmin(admin.ModelAdmin):
    model = CostCode
    list_display = ['program_name', 'cost_code',]

"""
class ProgramAdmin(admin.ModelAdmin):
    model = Program
    list_display = ['get_date', 'program_select', 'hours_spent',
                    'minutes_spent', 'notes', ] # 'get_date'

    list_editable = ['program_select', 'hours_spent',
                    'minutes_spent', 'notes', ] # Make editable

    def get_date(self, obj):
        return obj.time.date_select
    get_date.admin_order_field = 'time'
    get_date.short_description = 'Date'
"""

#admin.site.register(Program, ProgramAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(CostCode, CostCodeAdmin)
admin.site.register(Department)
admin.site.register(JobType)
