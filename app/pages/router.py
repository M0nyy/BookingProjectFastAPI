from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotel_by_location


router = APIRouter(prefix='/pages',
                   tags=['FRONTEND'])


templates = Jinja2Templates(directory='app/templates')


@router.get(path='/hotels')
async def get_hotels_page_by_location(request: Request, hotels=Depends(get_hotel_by_location)):
    return templates.TemplateResponse(name='hotels.html', context={'request': request, 'hotels': hotels})


