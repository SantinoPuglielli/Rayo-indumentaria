class UsuarioMiddleware:
    def _init_(self, get_response):
        self.get_response = get_response
    
    def _call_(self, request):
        # Agregar información del usuario a request
        request.usuario_logueado = request.session.get('usuario_id') is not None
        request.usuario_email = request.session.get('usuario_email')
        request.usuario_nombre = request.session.get('usuario_nombre')
        request.es_admin = request.session.get('es_admin', False)
        
        response = self.get_response(request)
        return response