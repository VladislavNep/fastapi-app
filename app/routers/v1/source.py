from typing import List
from fastapi import APIRouter, Security, Depends
from core.dependencies import security, is_authentication
from schemas.sources import Source
from services.sources import get_source_data


router = APIRouter()


@router.get(
    '/sources',
    response_model=List[Source],
    dependencies=[Security(security), Depends(is_authentication)]
)
async def get_list_source_data():
    data = await get_source_data()
    return data
