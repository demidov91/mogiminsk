from block_ip.decorators import api_key


class tg_api_key(api_key):
    def get_current_key(self, request):
        return request.query.getone('key', None)