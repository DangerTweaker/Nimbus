#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.http import Http404
from django.views.generic.create_update import update_object, create_object
from django.shortcuts import render_to_response as _render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext


from nimbus.shared import forms

def edit_singleton_model(request, templatename, redirect_to, 
                         formclass = None, model = None):

    if not formclass and model:
        formclass = forms.form(model)
    try:
        return update_object( request, object_id=1, 
                              form_class = formclass, 
                              model = model,
                              template_name = templatename, 
                              post_save_redirect = reverse(redirect_to) )
    except Http404, error:
        return create_object( request, 
                              form_class = formclass, 
                              model = model,
                              template_name = templatename, 
                              post_save_redirect = reverse(redirect_to) )



def render_to_response(request, template, dictionary ):
     return _render_to_response( template, dictionary,
                                context_instance=RequestContext(request))


