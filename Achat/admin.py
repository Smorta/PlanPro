from django.contrib import admin
from Achat.models import Responsable,Phase,User,Chantier,Modification
# Register your models here.
admin.site.register(Responsable)
admin.site.register(Phase)
admin.site.register(User)
admin.site.register(Chantier)
admin.site.register(Modification)