from django.contrib import admin
from .models import Event, Worker, Wristband, Bib, Tent, Role, Accredit, WorkerImage, BulkInsert
# Register your models here.
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('payroll_id','first_name', 'last_name', 'date_of_birth', 'employer', 'working_at')

class WorkerImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'is_active', 'accredit')


admin.site.register(Event)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Wristband)
admin.site.register(Bib)
admin.site.register(BulkInsert)
admin.site.register(Tent)
admin.site.register(Role)
admin.site.register(Accredit)
admin.site.register(WorkerImage, WorkerImageAdmin)