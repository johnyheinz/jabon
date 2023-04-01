from vkbottle.http import AiohttpClient

from chitchat.formating import clean_response, clean_request, get_excuse

# Адрес API сбера
API_URL = "https://api.aicloud.sbercloud.ru/public/v2/boltalka/predict"

context = {}

async def get(text, user_id) -> str:
    """Генерирует ответ на сообщение"""
    text = clean_request(text)
    if text is None:
        return get_excuse()

    if len(context[str(user_id)]) == 10:
        context[str(user_id)] = context[str(user_id)][:-8]
    context[str(user_id)].append(text)

    http = AiohttpClient()
    response = await http.request_json(
        API_URL,
        method="POST",
        json={"instances": [{"contexts": [context]}]},
    )
    await http.close()

    answer = response["responses"][2:-2]
    context[str(user_id)].append(answer)
    return clean_response(answer)