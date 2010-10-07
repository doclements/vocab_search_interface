#!/usr/bin/env python
""" vocabutils docstring TBD"""
__version__ = '0.0.1'

from suds.client import Client
from suds import WebFault as suds_fail
client = Client('http://vocab.ndg.nerc.ac.uk/1.1/VocabServerAPI_dl.wsdl')
 

def term2label(key=None):
    """ This method returns a the full title (string) for a Term based on its URI"""
    recordKey = key
    ret =  client.service.getList(recordKey)
    label = ret.codeTableRecord[0].entryTerm
    return label

def term2related(key=None, objectkey=None):
    """ this method returns an dict representing the related terms for the given URI """
    recordKey,objectKey = [], []
    mappings = {}
    recordKey.append(key)
    predicate = 255
    inference = 'true'
    ret = client.service.getRelatedRecordByTerm(recordKey, predicate, objectKey, inference)
    if hasattr(ret.codeTableRecord[0], 'minorMatch'): mappings['minorMatch'] = ret.codeTableRecord[0].minorMatch
    if hasattr(ret.codeTableRecord[0], 'exactMatch'): mappings['exactMatch'] = ret.codeTableRecord[0].exactMatch
    if hasattr(ret.codeTableRecord[0], 'broadMatch'): mappings['broadMatch'] = ret.codeTableRecord[0].broadMatch
    if hasattr(ret.codeTableRecord[0], 'narrowMatch'): mappings['narrowMatch'] = ret.codeTableRecord[0].narrowMatch
    return mappings

def list2name(list=None):
    """ this method will return a strung representing the name of the list supplied """
    name = 'not found'
    ret = client.service.whatLists()
    for tlist in ret.codeTableType:
        #print tlist
        if tlist.listKey==list:
            name = tlist.listLongName
    return name    

 