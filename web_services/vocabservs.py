import web
from suds.client import Client
from django.utils.encoding import smart_str, smart_unicode
from vocabutils import term2label, list2name



def dblist2name(list=None):
    myvar = dict(uri=list)
    results = db.select('lists', myvar, where="listuri = $uri")
    return results[0].listname

globals = {'term2label': term2label, 'list2name' : list2name, 'dblist2name' : dblist2name}
render = web.template.render('/var/www/web_services/templates', globals=globals,cache=True)
client = Client("http://vocab.ndg.nerc.ac.uk/axis2/services/vocab?wsdl")
db = web.database(dbn='sqlite', db='/var/www/web_services/vocablists')
web.config.debug = False


class gemet:
    def GET(self):
        i = web.input()
        query = i.q
        ob = getgemetmatches(q=query)
        return render.gemet(ob)


class nerc:
    def GET(self):
        i = web.input()
        query = i.q
        wild = 'off'
        if hasattr(i,'wild'):
            wild = i.wild
        num = 10
        if hasattr(i,'num'):
            num = i.num
        ob = getnercvocabmatches(q=query, n=num, w=wild)
        return render.results(ob)

class term:
    def GET(self):
        i = web.input()
        termin = i.term
        query = i.q
        ob = gettermdetails(term=termin, q=query)
        
        return render.term(ob)






def gettermdetails(term=None, q=None):
    """ this methods will return an object reflecting all of the metadata and related terms from within the vocabs """
    uri = "http://vocab.ndg.nerc.ac.uk/term/%s" % term
    meta = client.service.getRelatedRecordByTerm(uri, 255,None, 1 )
    list = meta.codeTableRecord[0]['listKey'].split("/")
    meta['list'] = list[4]
    meta['q'] = q
    if hasattr(meta.codeTableRecord[0], 'narrowMatch'):
       meta.codeTableRecord[0]['narrowMatch'] = sorted(meta.codeTableRecord[0]['narrowMatch'], key=lambda x: x.listKey, reverse=True)
    else:
        meta.codeTableRecord[0]['narrowMatch'] = []
    if hasattr(meta.codeTableRecord[0], 'minorMatch'):
        meta.codeTableRecord[0]['minorMatch'] = sorted(meta.codeTableRecord[0]['minorMatch'], key=lambda x: x.listKey, reverse=True)
    else:
        meta.codeTableRecord[0]['minorMatch'] = []
    if hasattr(meta.codeTableRecord[0], 'broadMatch'):
        meta.codeTableRecord[0]['broadMatch'] = sorted(meta.codeTableRecord[0]['broadMatch'], key=lambda x: x.listKey, reverse=True)
    else:
        meta.codeTableRecord[0]['broadMatch'] = []
    if hasattr(meta.codeTableRecord[0], 'exactMatch'):
       meta.codeTableRecord[0]['exactMatch'] = sorted(meta.codeTableRecord[0]['exactMatch'], key=lambda x: x.listKey, reverse=True)
    else:
        meta.codeTableRecord[0]['exactMatch'] = []
    
    return meta


def getnercvocabmatches(q=None, n=5, w=None):
    """ this method retrieves a suds object that is iterable from the nerc vocad searchVocab method """
    from suds.client import Client
    from datetime import datetime
    start =  datetime.now()
    nercret = {}
    if w!='on':
        q = "*%s*" % q
        nercret['wild'] = 'on'
    else:
        q = q
        nercret['wild'] = 'off'
    #client = Client("http://vocab.ndg.nerc.ac.uk/axis2/services/vocab?wsdl")
    result = client.service.searchVocab('',q,0,'')
    
    nercret['count'] = 0
    nercret['q'] = q
    nercret['listcount'] = 0
    nercret['results'] = []
    nercret['num'] = n
    seq = []
    codeitem = client.factory.create('ns0:codeTableRecordType')
    if hasattr(result, 'codeTableRecord'):
        nercret['count'] = len(result['codeTableRecord'])
        for item in result['codeTableRecord']:
            seq.append(item.listKey)
            
        
        nercret['listcount'] = len(f5(seq))
        for item in result['codeTableRecord']:
            codeitem = item
            list = codeitem['listKey'].split("/")
            termuri = codeitem['entryKey'].split("/") 
            codeitem['list'] = list[4]
            codeitem['uri'] = "/".join(termuri[4:])
            if codeitem['entryTermAbbr'] == None:
                codeitem['entryTermAbbr'] = 'none'
            if codeitem['entryTermDef'] == None:
                codeitem['entryTermDef'] = 'none'
            nercret['results'].append(codeitem)
    end =  datetime.now()
    dur = end - start
    nercret['duration'] = "%s.%s" % (str(dur.seconds), str(dur.microseconds)[0:2])
    return nercret

def f5(seq, idfun=None): 
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

def getgemetmatches(q=None):
    """ this method retrieves a json object from the gemet getrelatedconcepts REST method """
    import urllib
    
    # Get a file-like object for the Python Web site's home page.
    f = urllib.urlopen("http://www.eionet.europa.eu/gemet/getConceptsMatchingKeyword?keyword=%s&search_mode=3&thesaurus_uri=http://www.eionet.europa.eu/gemet/concept/&language=en" % q)
    # Read from the object, storing the page's contents in 's'.
    s  = f.read()
    objs = {}
    if(s):
        objs = eval(s)
    #list = []
    #for item in objs:
    #    list.append(item['preferredLabel']['string'])
    f.close()
    return objs


