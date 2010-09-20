# -*- coding: UTF-8 -*-
# Create your views here.

import simplejson

from django.views.generic import create_update
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from nimbus.computers.models import Computer
from nimbus.procedures.models import Profile, Procedure
from nimbus.storages.models import Storage
from nimbus.schedules.models import Schedule
from nimbus.filesets.models import FileSet
from nimbus.backup.forms import StorageForm

from nimbus.shared.enums import days, weekdays, levels, operating_systems

def backup_form(request, object_id=None):
    if object_id:
        computer = Computer.objects.get(id=object_id)
    else:
        computer = None
    
    computers = Computer.objects.all()
    profiles = Profile.objects.all()
    storages = Storage.objects.all()
    schedules = Schedule.objects.all()
    filesets = FileSet.objects.all()
    
    extra_context = {
        'title': u"Criar Backup",
        'computer': computer,
        'computers': computers,
        'profiles': profiles,
        'storages': storages,
        'days': days,
        'weekdays': weekdays,
        'levels': levels,
        'operating_systems': operating_systems,
        'schedules': schedules,
        'filesets': filesets,
    }
    return create_update.create_object( request, 
                                        form_class = StorageForm,
                                        template_name = "backup_create.html",
                                        extra_context = extra_context,
                                        post_save_redirect = "/computers/")


def add(request):
    if request.method == "POST":
        print request.POST
        # import pdb; pdb.set_trace()
        
        ### Campos que serão recebidos nesta função:
        
        # procedure_name - str
        # computer_id - int
        # profile_id - int
        # 
        # profile.storage_id - int
        # profile.schedule_id - int
        # profile.fileset_id - int
        # 
        # schedule.name - str
        # 
        # schedule.monthly.active - bool
        # schedule.monthly.day - list
        # schedule.monthly.hour - str
        # schedule.monthly.level - int
        # 
        # schedule.weekly.active - bool
        # schedule.weekly.day - list
        # schedule.weekly.hour - str
        # schedule.weekly.level - int
        # 
        # schedule.dayly.active - bool
        # schedule.dayly.day - list
        # schedule.dayly.hour - str
        # schedule.dayly.level - int
        # 
        # schedule.hourly.active - bool
        # schedule.hourly.day - list
        # schedule.hourly.hour - str
        # schedule.hourly.level - int
        
        ## Exemplo do objeto.
        # {
        # u'schedule.monthly.level': [u'Full'],
        # u'procedure_name': [u'asdasdas'],
        # u'schedule.dayly.level': [u'Full'],
        # u'profile.schedule_id': [u'Criar novo agendamento'],
        # u'schedule.weekly.active': [u'1'],
        # u'schedule.dayly.hour': [u''],
        # u'computer_id': [u'1'],
        # u'schedule.weekly.level': [u'Full'],
        # u'profile_id': [u''],
        # u'profile.fileset_id': [u'2'],
        # u'schedule.hourly.minute': [u''],
        # u'fileset_name': [u'', u'', u''],
        # u'schedule.monthly.hour': [u'13:00'],
        # u'profile.storage_id': [u'1'],
        # u'schedule.weekly.day[]': [u'mon', u'wed'],
        # u'schedule.hourly.level': [u'Full'],
        # u'schedule.weekly.hour': [u'21:00'],
        # u'schedule.monthly.day[]': [u'1', u'17', u'29'],
        # u'schedule.monthly.active': [u'1']
        # }


def get_tree(request):
    path = request.POST['path']
    computer_id = request.POST['computer_id']
    
    # files = Procedure.locate_files(job_id, path)
    files = ["D:/Dados/", "D:/Pessoal/", "D:/Fotos/"]

    response = simplejson.dumps(files)
    return HttpResponse(response, mimetype="text/plain")
    
