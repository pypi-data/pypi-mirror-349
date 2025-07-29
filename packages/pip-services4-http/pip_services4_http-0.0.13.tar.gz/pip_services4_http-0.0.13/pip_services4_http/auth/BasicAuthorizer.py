# -*- coding: utf-8 -*-
from typing import Callable

import bottle
from pip_services4_commons.errors import UnauthorizedException

from pip_services4_http.controller.HttpResponseSender import HttpResponseSender


class BasicAuthorizer:

    def anybody(self) -> Callable:
        return lambda: None

    def signed(self) -> Callable:
        def inner():
            user = bottle.request.environ.get('bottle.request.ext.user')
            if user is None:
                raise bottle.HTTPResponse(body=HttpResponseSender.send_error(UnauthorizedException(
                    None,
                    'NOT_SIGNED',
                    'User must be signed in to perform this operation '
                ).with_status(401)), status=401, headers={
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Authorization, Content-Type',
                    'Cache-Control': 'no-store, no-cache, must-revalidate',
                    'Pragma': 'no-cache'
                })
        return inner
