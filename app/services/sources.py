import json
import numpy as np
import os
from operator import itemgetter
import aiofiles
from core.config import settings


async def get_source_data():
    sources_file_path = [
        os.path.join(settings.BASE_DIR, 'data/source_1.json'),
        os.path.join(settings.BASE_DIR, 'data/source_2.json'),
        os.path.join(settings.BASE_DIR, 'data/source_3.json'),
        ]
    result = list()
    # Динамически вызываю файлы, дабы не пложить код, ибо их может быть много
    for file_name in sources_file_path:
        data = await get_data_from_json_file(filename=file_name)
        result.append(data)

    # склеиваю масивы в один и выравниваю по горизонтали
    # ex: было [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    # ex: стало [1, 1, 1, 2, 2, 2, 3, 3, 3]
    result = np.hstack(result).ravel()
    # сортирую по полю id и выдаю результат
    return sorted(result, key=itemgetter('id'))


async def get_data_from_json_file(filename: str) -> dict:
    async with aiofiles.open(filename, 'r', encoding='utf-8') as file:
        data = await file.read()

    return json.loads(data)

