from functools import wraps
from flask import request, jsonify, g

def get_current_tenant_id():
    # Se for superadmin com query param ou header para suporte/impersonate
    if getattr(g, 'user_role', None) == 'superadmin':
        impersonate_tenant = request.headers.get('X-Tenant-ID') or request.args.get('tenant_id')
        if impersonate_tenant:
            return impersonate_tenant
    return getattr(g, 'current_tenant_id', None)

def require_tenant(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        tenant_id = get_current_tenant_id()
        if not tenant_id:
            return jsonify({'error': 'Contexto de empresa (tenant) não identificado'}), 400
        g.tenant_id = tenant_id
        return f(*args, **kwargs)
    return decorated
