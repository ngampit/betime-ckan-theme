import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
import ckan.authz as authz
import ckan.logic.auth as logic_auth
import ckan.plugins as p
import datetime as datetime
def date_range():
    return list(reversed(range(2019,datetime.datetime.now().year+1)))

class BtThemePlugin(plugins.SingletonPlugin):
    # plugins.implements(plugins.IConfigurer)
    # plugins.implements(plugins.IAuthFunctions)
    # IConfigurer
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers)
    
        
    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'date_range':date_range
        }
    def after_map(self, map):
        
    
        map.connect('masterconnection', '/master_connection',
            controller='ckanext.bt_theme.controller:MasterConnectionController',
            action='index')
        map.connect('masterconnection', '/add_master_connection',
            controller='ckanext.bt_theme.controller:MasterConnectionController',
            action='add_master')
        map.connect('masterconnection', '/edit_master_connection/:id',
            controller='ckanext.bt_theme.controller:MasterConnectionController',
            action='edit_master')
        map.connect('masterconnection', '/masterdata/dataset/:name',
            controller='ckanext.bt_theme.controller:MasterConnectionController',
            action='master_dataset')
        return map
    

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic','bt_theme')

   
    

# IAuthFunctions 
    # def get_auth_functions(self):
    #     auth_functions = {
    #         'user_generate_apikey': self.user_generate_apikey
    #     }
    #     return auth_functions
    
    # def user_generate_apikey(self, context, data_dict):
    #     user = context['user']
    #     user_obj = logic_auth.get_user_object(context, data_dict)
    #     if user == user_obj.name:
    #         # Allow users to update only their own user accounts.
    #         return {'success': True}
    #     return {'success': False, 'msg': _('User {0} not authorized to update user'
    #             ' {1}'.format(user, user_obj.id))}