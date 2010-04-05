#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import string

from django.core import serializers
from django.db import models
from django import forms

from backup_corporativo.bkp.models import TYPE_CHOICES, LEVEL_CHOICES, OS_CHOICES, DAYS_OF_THE_WEEK
from backup_corporativo.bkp import customfields as cfields
from backup_corporativo.bkp import utils


class NetworkInterface(models.Model):
    interface_name = cfields.ModelSlugField("Nome da Interface", max_length=30)
    interface_address = models.IPAddressField("Endereço IP")
    interface_netmask = models.IPAddressField("Máscara")
    interface_network = models.IPAddressField("Network")
    interface_broadcast = models.IPAddressField("Broadcast")
    interface_gateway = models.IPAddressField("Gateway Padrão")
    interface_dns1 = models.IPAddressField("Servidor DNS 1")
    interface_dns2 = models.IPAddressField("Servidor DNS 2")

    # Classe Meta é necessária para resolver um problema gerado quando se
    # declara um model fora do arquivo models.py. Foi utilizada uma solução
    # temporária que aparentemente funciona normalmente. 
    # Para mais informações sobre esse hack, acessar ticket:
    # http://code.djangoproject.com/ticket/4470
    # NOTA: No momento em que esse código foi escrito, o Django estava
    # na versão "Django-1.0.2-final" e uma alteração no core do Django
    # estava sendo discutida em paralelo, mas o ticket ainda encontrava-se em
    # aberto e portanto ainda sem solução definitiva.
    # Caso um dia a aplicação venha a quebrar nesse trecho do código por conta
    # de uma atualização para uma versão do Django superior a 1.0.2,
    # vale a pena verificar se alguma alteração foi realmente realizada
    # nessa nova versão do Django.
    # Para mais informações sobre essa correção, acessar ticket:
    # http://code.djangoproject.com/ticket/3591
    class Meta:
        app_label = 'bkp'    

    
    def save(self, *args, **kwargs):
        from backup_corporativo.bkp.app_models.storage import Storage
        sto = Storage.get_instance()
        sto.storage_name = "Storage Local"
        sto.storage_ip = self.interface_address
        sto.save()
        self.id = 1
        super(NetworkInterface, self).save(*args, **kwargs)


    def __unicode__(self):
        return "%s (%s)" % (self.interface_name, self.interface_address)
        
    @classmethod
    def get_instance(cls):
        try:
            netconfig = cls.objects.get(pk=1)
            return netconfig
            iface = cls.objects.get(pk=1)
            return iface
        except cls.DoesNotExist:
            return cls()
