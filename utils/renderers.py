#rest_frame files
from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context :
            if isinstance(data, dict):
                message = data.pop('message', 'successfully')
                status_code = data.pop('status_code', renderer_context['response'].status_code)
            else:
                message = 'successfully'
                status_code = renderer_context['response'].status_code
            custom_response = {
                'message': message,
                'status_code': status_code,
                'data': data,
            }
            return super().render(custom_response, accepted_media_type, renderer_context)
        return super().render(data, accepted_media_type, renderer_context)
















