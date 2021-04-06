from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
    verbose_name = "Songolmae Database"
    
class ApisConfig(AppConfig):
    name = 'apis'
    verbose_name = "Songolmae Database"