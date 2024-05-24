from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User, Product
from schema import ProductModel
from database import session, engine
from fastapi.encoders import jsonable_encoder
product_router = APIRouter(
    prefix='/product'
)

session = session(bind=engine)


@product_router.post('/create/', status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Enter a invalid access token')
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    if current_user:
        new_product = Product(
            name=product.name,
            price=product.price
        )
        session.add(new_product)
        session.commit()
        data = {
            'success': True,
            'code': 201,
            'message': 'Product is successfully created',
            'data': {
                'id': new_product.id,
                'name': new_product.name,
                'price': new_product.price,
            }
        }
        return jsonable_encoder(data)
    raise HTTPException(detail=f'only Super Admin can  new product add', status_code=status.HTTP_403_FORBIDDEN)