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
    data = {
        'success': True,
        'code': 201,
        'message': 'Order created successfully',
        'data': {
            'id': new_order.id,
            'qty': new_order.qty,
            'order_status': new_order.order_status,
        }
    }

    return jsonable_encoder(data)

@order_router.get('/list/', status_code=status.HTTP_200_OK)
async def list_order(Authorize: AuthJWT= Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()   

    if user:
        orders = session.query(Order).all()
        custom_data = [
            {
                'id': order.id,
                'user': {
                    'id': order.user.id,
                    'username': order.user.username,
                    'email': order.user.email,
                    'is_staff': order.user.is_staff,
                    'is_active': order.user.is_active,
                },
                'product_id': order.product_id,
                'quantity': order.qty,
                'order_statuses': order.order_status.value

            }
            for order in orders
        ]
        return jsonable_encoder(custom_data)
    else:
        raise HTTPException(detail=f'only Super Admin can see all orders', status_code=status.HTTP_403_FORBIDDEN)



@order_router.get('/{id}/')
async def get_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)
    
    user = Authorize.get_jwt_subject()
    print(user)
    current_user = session.query(User).filter(User.username == user).first()
    print(id)

    if current_user:
        order = session.query(Order).filter(Order.id == id).first()
        custom_order = {
                'id': order.id,
                'user': {
                    'id': order.user.id,
                    'username': order.user.username,
                    'email': order.user.email,
                    'is_staff': order.user.is_staff,
                    'is_active': order.user.is_active,
                },
                'product_id': order.product_id,
                'quantity': order.qty,
                'order_statuses': order.order_status.value

            }
        return jsonable_encoder(custom_order)
    raise HTTPException(detail=f'only Super Admin is allowed to this request', status_code=status.HTTP_403_FORBIDDEN)