#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def script_name(request):
    # return { 'script_name' : request.META['SCRIPT_NAME']} 
    return { 'script_name' : request.META['PATH_INFO']}

# Exemplo.
# def computers(request):
#     # return { 'script_name' : request.META['SCRIPT_NAME']} 
#     return { 'computers' : 12312}