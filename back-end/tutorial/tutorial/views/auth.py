from pyramid.csrf import new_csrf_token
from pyramid.httpexceptions import HTTPSeeOther
from pyramid.security import (
    remember,
    forget,
)
from pyramid.response import Response
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from .. import models

@view_config(route_name='login', request_method='POST')
def login(request):
    try:
        json_data = request.json_body
        username = json_data.get('user')
        password = json_data.get('password')

        user = request.dbsession.query(models.User).filter_by(name=username).first()
        
        if user is not None and user.check_password(password):
            # csrf_token = new_csrf_token(request)
            next_url = request.route_url('dashboard')
            headers = remember(request, user.id)
            response = {
                'message': 'OK',
                'next_url': next_url
                # 'token': csrf_token
            }
            return Response(json=response, status=200, headers=headers)
        else:
            next_url = request.route_url('login')
            response = {
                'message': 'Failed login',
                'next_url': next_url
                # 'token': csrf_token
            }
            return Response(json=response, status=400)

    except Exception as e:
        message = str(e)
        return Response(
            json={
                "msg": message
            },
            status=500
        )


@view_config(route_name='logout', request_method='POST')
def logout(request):
    next_url = request.route_url('dashboard')
    # new_csrf_token(request)
    print(request.method)
    if request.method != 'POST':
        response = {
            'message': 'Failed Logout',
            'next_url': next_url
            # 'token': csrf_token
        }
        return Response(json=response)
    else:
        next_url = request.route_url('login')
        headers = forget(request)
        response = {
            'message': 'OK',
            'next_url': next_url
            # 'token': csrf_token
        }
        return Response(json=response, headers=headers)

@forbidden_view_config(renderer='json')
def forbidden_view(exc, request):
    if not request.is_authenticated:
        next_url = request.route_url('login', _query={'next': request.url})
        return HTTPSeeOther(location=next_url)

    request.response.status = 403
    data = {'message': 'access denied'}
    return data