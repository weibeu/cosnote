from flask import session, jsonify

import functools


def requires_authorization(view):
    @functools.wraps(view)
    def decorator(*args, **kwargs):
        if not session.get("username"):
            jsonify(errors=dict(message=["Unauthorized"]))
        return view(*args, **kwargs)
    return decorator
