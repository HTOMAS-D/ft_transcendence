from django.db import models

# Create your models here.

#Monitoring your models
#You may want to monitor the creation/deletion/update rate for your model. 
# This can be done by adding a mixin to them. This is safe to do on existing models (it does not require a migration).
# ExportModelOperationsMixin('dog') ---->add this before models.Model in the wanted model
