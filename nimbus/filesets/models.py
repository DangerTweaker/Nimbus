#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from os import path

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete, m2m_changed

from nimbus.base.models import BaseModel
from nimbus.shared import utils, signals, fields
from nimbus.libs.template import render_to_file

# Create your models here.



class FileSet(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __unicode__(self):
        return self.name


class FilePath(models.Model):
    path = fields.ModelPathField(max_length=255, null=False, unique=True)
    filesets = models.ManyToManyField(FileSet, related_name="files", null=True, blank=True)

    def __unicode__(self):
        return self.path




def update_fileset_file(fileset):
    """FileSet update filesets to a procedure instance"""

    name = fileset.bacula_name

    filename = path.join( settings.NIMBUS_FILESETS_DIR, 
                          name)

    render_to_file( filename,
                    "fileset",
                    name=name,
                    files=[ f.path for f in fileset.files.all() ])




def remove_fileset_file(fileset):
    """remove FileSet file"""

    name = fileset.bacula_name
    filename = path.join( settings.NIMBUS_FILESETS_DIR, 
                          name)
    utils.remove_or_leave(filename)    



def update_filepath(filepath):
    for fileset in filepath.filesets.all():
        update_fileset_file(fileset)




signals.connect_on( update_fileset_file, FileSet, post_save)
signals.connect_on( remove_fileset_file, FileSet, post_delete)
signals.connect_on( update_filepath, FilePath.filesets.through, m2m_changed)
#signals.connect_m2m_on( update_filepath, FilePath.filesets.through, m2m_changed)