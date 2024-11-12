from rest_framework.renderers import JSONRenderer
import json


class UTF8JSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Конвертируем данные JSON в строку с ensure_ascii=False
        response_data = json.dumps(data, ensure_ascii=False)
        # Преобразуем строку в байты с кодировкой utf-8 и возвращаем
        return response_data.encode('utf-8')
