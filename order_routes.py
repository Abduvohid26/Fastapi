from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User, Product, Order
from schema import OrderModel, OrderStatus
from database import session, engine
from fastapi.encoders import jsonable_encoder
order_router = APIRouter(
    prefix='/order'
)

session = session(bind=engine)

@order_router.get('/')
async def welcome_page(Authorize: AuthJWT= Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid token {str(e)}'
        )
    return {'message' :'This is page order'}

@order_router.post('/make/', status_code=status.HTTP_200_OK)
async def make_order(order: OrderModel, Authorize: AuthJWT= Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid token {str(e)}'
        )
    current_user = Authorize.get_jwt_subject()
    print('curr', current_user)
    user = session.query(User).filter(User.username == current_user).first()
    new_order = Order(
        qty = order.qty,
        # product = order.product_id,
    )
    new_order.user = user
    session.add(new_order)
    session.commit()
    response = {
        'id': new_order.id,
        'qty': new_order.qty,
        'order_status': new_order.order_status,
    }
    return jsonable_encoder(response)


