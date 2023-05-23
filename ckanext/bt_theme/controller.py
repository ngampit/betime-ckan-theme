import ckan.plugins as p
import ckan.lib.base as base
from ckan.lib.base import BaseController, config
import time
from logging import getLogger
import http.client
import ckan.model as model
import ckan.logic as logic
import ckan.authz as authz
import ckan.lib.helpers as h

get_action = logic.get_action

log = getLogger(__name__)

class MasterConnectionController(BaseController):
  
    def timed(self, f, arg = None):
        start = time.time()
        if arg:
            ret = f(arg)
        else:
            ret = f()
        elapsed = time.time() - start
        log.info(f.__name__ +" "+ str(elapsed) + ' seconds')
        return ret
 
    def index(self):
         c = p.toolkit.c
    #    conn = http.client.HTTPSConnection("localhost")
    #    payload = ''
    #    headers = {}
    #    conn.request("GET", "/api/master", payload, headers)
    #    res = conn.getresponse()
    #    data = res.read()
    #    c.data_json = "sss"
         
         try:
            context_user = dict(model=model, user=c.user, auth_user_obj=c.userobj)
            logic.check_access(u'sysadmin', context_user)
         except logic.NotAuthorized:
            return h.redirect_to(u'/')

         return p.toolkit.render('master_connection.html')
    
    def add_master(self): 
         c = p.toolkit.c
         try:
            context_user = dict(model=model, user=c.user, auth_user_obj=c.userobj)
            logic.check_access(u'sysadmin', context_user)
         except logic.NotAuthorized:
            return h.redirect_to(u'/')

         return p.toolkit.render('add_master_connection.html')
    
    def edit_master(self,id):
       c = p.toolkit.c
       c.id=id

       try:
            context_user = dict(model=model, user=c.user, auth_user_obj=c.userobj)
            logic.check_access(u'sysadmin', context_user)
       except logic.NotAuthorized:
            return h.redirect_to(u'/')

       return p.toolkit.render('edit_master_connection.html')
    
    def master_dataset(self,name):
      c = p.toolkit.c
      c.name=name
      context = {
        u'model': model,
        u'session': model.Session,
        u'user': c.user, 
        u'auth_user_obj': c.userobj,
        u'for_view': True
      }
      
      try:
            context_user = dict(model=model, user=c.user, auth_user_obj=c.userobj)
            logic.check_access(u'sysadmin', context_user)
      except logic.NotAuthorized:
            return h.redirect_to(u'/')      

      c.pks = get_action(u'package_show')(context, {u'id': c.name})
      return p.toolkit.render('master_dataset.html')
