from django.contrib import admin

from task_manager.models import Task, Status, Label, LabelTaskIntermediate

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'creation_date', 'author',
                    'author_id', 'executor', 'executor_id',
                    'status', 'status_id')
    list_display_links = ('id', 'author')
    search_fields = ('name', 'author')
    list_editable = ('name', 'description')
    list_filter = ('author', 'status')
    save_on_top = True

class LabelTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'label_link', 'task_link')


admin.site.register(Task, TaskAdmin)
admin.site.register(Status)
admin.site.register(Label)
admin.site.register(LabelTaskIntermediate, LabelTaskAdmin)

admin.site.site_title = 'Админ-панель менеджера задач'
admin.site.site_header = 'Админ-панель менеджера задач 2'
