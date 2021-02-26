import json
import odoo
from odoo import api, http, SUPERUSER_ID
from odoo.http import request
import passlib.context


DEFAULT_CRYPT_CONTEXT = passlib.context.CryptContext(
    # kdf which can be verified by the context. The default encryption kdf is
    # the first of the list
    ['pbkdf2_sha512', 'plaintext'],
    # deprecated algorithms are still verified as usual, but ``needs_update``
    # will indicate that the stored hash should be replaced by a more recent
    # algorithm. Passlib 1.6 supports an `auto` value which deprecates any
    # algorithm but the default, but Ubuntu LTS only provides 1.5 so far.
    deprecated=['plaintext'],
)

DATABASE_NAME = 'demo002'

LOGIN_ROUTER = ['/api/v1.0/user/login']
CHANGE_PASSWORD_ROUTER = ['/api/v1.0/user/change_password']
GET_INFO_ROUTER = ['/api/v1.0/user/get_info']
LOGOUT_ROUTER = ['/api/v1.0/user/logout']


class HubUser(http.Controller):
    @http.route(LOGIN_ROUTER, type="http", auth="none", methods=['POST'], cors='*', csrf=False)
    def hub_user_login(self, **kwargs):
        """
        登陆验证
        :param kwargs:
        :return:
        """
        user_obj = request.env['res.users'].sudo()
        user_cls = odoo.registry(DATABASE_NAME)['res.users']
        res_data = []
        if kwargs.get('username') and kwargs.get('password'):
            login = user_cls._login(DATABASE_NAME, kwargs.get('username'), kwargs.get('password'))
            if login:
                user = user_obj.browse(login)
                res_data.append({'id': user.id, 'name': user.login})
                return json.dumps({'code': 0, 'message': 'success', 'data': res_data})
            else:
                return json.dumps({'code': 1, 'message': 'fail', 'info': '用户名或密码无效', 'data': res_data})
        else:
            return json.dumps({'code': 1, 'message': 'fail', 'info': '用户名或密码不能为空', 'data': res_data})

    @http.route(CHANGE_PASSWORD_ROUTER, type="http", auth="none", methods=['POST'], cors='*', csrf=False)
    def hub_change_password(self, **kwargs):
        """
        密码修改
        :param kwargs:
        :return:
        """
        user_obj = request.env['res.users'].sudo()
        user_cls = odoo.registry(DATABASE_NAME)['res.users']
        user_id = kwargs.get('user_id') or request.session.uid
        res_data = []
        if user_id and kwargs.get('old_password') and kwargs.get('new_password'):
            user = user_obj.browse(int(user_id))
            valid = user_cls._login(DATABASE_NAME, user.login, kwargs.get('old_password'))
            if valid:
                user.password = DEFAULT_CRYPT_CONTEXT.encrypt(kwargs.get('new_password'))
                res_data.append({'id': user.id, 'name': user.login, 'password': kwargs.get('new_password')})
                return json.dumps({'code': 0, 'message': 'success', 'data': res_data})
            else:
                return json.dumps({'code': 1, 'message': 'fail', 'info': '原始密码无效', 'data': res_data})
        else:
            return json.dumps({'code': 1, 'message': 'fail', 'info': '原始密码或新密码不能为空', 'data': res_data})

    @http.route(GET_INFO_ROUTER, type="http", auth="none", methods=['POST'], cors='*', csrf=False)
    def hub_get_info(self, **kwargs):
        """
        查询用户信息
        :param kwargs:
        :return:
        """
        user_obj = request.env['res.users'].sudo()
        user_id = kwargs.get('user_id') or request.session.uid
        res_data = []
        if user_id:
            user = user_obj.browse(int(user_id))
            if user:
                res_data.append({'id': user.id, 'name': user.login})
                return json.dumps({'code': 0, 'message': 'success', 'data': res_data})
            else:
                return json.dumps({'code': 1, 'message': 'fail', 'info': None, 'data': res_data})
        else:
            return json.dumps({'code': 1, 'message': 'fail', 'info': None, 'data': res_data})

    @http.route(LOGOUT_ROUTER, type="http", auth="none", methods=['GET'], cors='*', csrf=False)
    def hub_logout(self, **kwargs):
        """
        退出登陆
        :param kwargs:
        :return:
        """
        res_data = []
        try:
            request.session.logout(keep_db=False)
            return json.dumps({'code': 0, 'message': 'success', 'data': res_data})
        except Exception as e:
            return json.dumps({'code': 1, 'message': 'fail', 'info': e, 'data': res_data})
