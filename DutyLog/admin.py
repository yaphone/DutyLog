from django.contrib import admin

# Register your models here.
from .models import RoleTable, DutyInfo, ContentTable, InstructionTable, ProxyInstructionTable, ResultTable


admin.site.register(RoleTable)
admin.site.register(DutyInfo)
admin.site.register(InstructionTable)
admin.site.register(ContentTable)
admin.site.register(ProxyInstructionTable)
admin.site.register(ResultTable)
