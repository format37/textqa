# Text QA
# https://demo.deeppavlov.ai/#/ru/textqa

import asyncio
from aiohttp import web
from deeppavlov import build_model, configs
import os
import json


print('loading model')
model = build_model(configs.squad.squad_ru, download=True)
print('Model load complete')
#model = build_model(configs.squad.squad_ru_rubert_infer, download=True)
#model = build_model(configs.squad.squad_ru_bert_infer, download=True)


async def call_test(request):
	content = "ok"	
	return web.Response(text=content,content_type="text/html")


async def call_textqa(request):	
        response = ''
        request_str = json.loads(str(await request.text()))
        request = json.loads(request_str)	
        if not 'texts' in request.keys():
                response += 'Parameter not found in request: texts\n'
        if not 'questions' in request.keys():
                response += 'Parameter not found in request: questions\n'
        if response == '':
                response = model(request['texts'], request['questions'])
        response = json.dumps(response)
        return web.Response(text=str(response),content_type="text/html")


def main():
        app = web.Application(client_max_size=1024**3)
        app.router.add_route('GET', '/test', call_test)
        app.router.add_post('/textqa', call_textqa)
        port=os.environ.get('PORT', '')
        print('Started at port', port)
        web.run_app(app, port=port)


if __name__ == "__main__":
	main()
