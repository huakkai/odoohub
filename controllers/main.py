import json
from odoo import http
from odoo.http import request

API_RESULT = {
    'success': 0,
    'fail': 1,
}

USER_ROUTER = ['/api/v1.0/user', '/api/v1.0/user/<int:user_id>']
Model_ROUTER = ['/api/v1.0/model', '/api/v1.0/model/<int:model_id>']


def get_return(result=None, res_data=[], info=None):
    ret_dict = {'data': res_data}
    if result:
        ret_dict = {
            **ret_dict,
            **{
                'code': API_RESULT.get('success'),
                'message': 'success'
            }
        }
    else:
        if info:
            ret_dict = {
                **ret_dict,
                **{
                    'code': API_RESULT.get('fail'),
                    'message': info
                }
            }
        else:
            ret_dict = {
                **ret_dict,
                **{
                    'code': API_RESULT.get('fail'),
                    'message': 'fail'
                }
            }
    return json.dumps(ret_dict)


class HubUser(http.Controller):
    @http.route(USER_ROUTER, type="http", auth="none", methods=['GET'])
    def hub_get_user(self, **kwargs):
        user_obj = request.env['res.users'].sudo()
        res_data = []
        if kwargs.get('user_id'):
            current_user = user_obj.browse(kwargs.get('user_id'))
            res_data.append({'id': kwargs.get('user_id'), 'name': current_user.name})
        else:
            res_data.append({'id': None, 'name': None})
        return json.dumps({'code': 0, 'message': 'success', 'data': res_data})


class HubModel(http.Controller):
    @http.route(Model_ROUTER, auth='none', type='http', cors='*', csrf=False)
    def hub_get_model(self):
        try:
            model_obj = http.request.env['ir.module.module'].sudo()
            models = model_obj.search([], limit=10)
            res_data = []
            for model in models:
                res_data.append({'id': model.id, 'name': model.name})
            return get_return(result=True, res_data=res_data)
        except Exception as e:
            return get_return(result=False, res_data=[], info=e)
