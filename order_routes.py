from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User, Product, Order
from schema import OrderModel, OrderStatusModel
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
        product_id = order.product_id,
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
            'product': {
                'id': new_order.product.id,
                'name': new_order.product.name,
                'price': new_order.product.price,
            },
            'total_price': new_order.qty * new_order.product.price
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
                'product': {
                    'id': order.product.id,
                    'name': order.product.name,
                    'price': order.product.price,
                },
                'quantity': order.qty,
                'order_statuses': order.order_status.value,
                'total_price': order.qty * order.product.price,

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
                'product': {
                    'id': order.product_id,
                    'name': order.product.name,
                    'price': order.product.price,
                },
                'quantity': order.qty,
                'order_statuses': order.order_status.value,
                'total_price': order.qty * order.product.price,

            }
        return jsonable_encoder(custom_order)
    raise HTTPException(detail=f'only Super Admin is allowed to this request', status_code=status.HTTP_403_FORBIDDEN)


@order_router.delete('/{id}/', status_code=status.HTTP_200_OK)
async def delete_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    order = session.query(Order).filter(Order.id == id).first()
    if order.user != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to delete this order')
    if order.order_status != 'PENDING':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Kechirasiz siz yo\'lga chiqqan buyurmatalrni ochira olmaysiz')
    session.delete(order)
    session.commit()
    data = {
        'success': True,
            'code': 200,
            'message': 'Order successfully deleted!',
            'data': None
        }
    return jsonable_encoder(data)


# @order_router.put('/{id}/', status_code=status.HTTP_200_OK)
# async def update_order_by_id(id: int, update_order: OrderModel, Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#     except Exception as e:
#         raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)
#     user = Authorize.get_jwt_subject()
#     current_user = session.query(User).filter(User.username == user).first()
#     if current_user:
#         order = session.query(Order).filter(Order.id == id).first()
#         if order:
#             for key, value in update_order.dict(exclude_unset=True).items():
#                 setattr(order, key, value)
#             session.commit()
#             data = {
#                 'id': order.id,
#                 'qty': order.qty,
#                 'status': order.order_status.value
#             }
#             return jsonable_encoder(data)
#         else:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only Super Admin is allowed to update orders')
@order_router.put('/{id}/', status_code=status.HTTP_200_OK)
async def put_order_by_id(id: int, update_order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    order = session.query(Order).filter(Order.id == id).first()
    if order.user != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to update this order')
    order.qty = update_order.qty
    order.product_id = update_order.product_id
    session.commit()
    custom_response = {
        'success': True,
        'code': 200,
        'message': 'Siznig buyurtmangiz successfully updated',
        'data': {
            'id': order.id,
            'qty': order.qty,
            'product_id': order.product_id,
            'order_status': order.order_status.value
        }
    }
    return jsonable_encoder(custom_response)
    


@order_router.patch('/{id}/', status_code=status.HTTP_200_OK)
async def patch_order_by_id(id: int, update_order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    if current_user:
        order = session.query(Order).filter(Order.id == id).first()
        if order:
            for key, value in update_order.dict(exclude_unset=True).items():
                setattr(order, key, value)
            session.commit()
            data = {
                'id': order.id,
                'qty': order.qty,
                'order_status': order.order_status.value
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only Super Admin is allowed to update orders')


@order_router.get('/user/orders/', status_code=status.HTTP_200_OK)
async def get_user_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    if current_user:
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
                    'product': {
                        'id': order.product.id,
                        'name': order.product.name,
                        'price': order.product.price,
                    },
                    'quantity': order.qty,
                    'order_statuses': order.order_status.value,
                    'total_price': order.qty * order.product.price,

                }
                for order in current_user.orders
            ]
        return jsonable_encoder(custom_data)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only user is allowed to see his orders')


@order_router.get('/user/orders/{id}/', status_code=status.HTTP_200_OK)
async def get_user_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    order = session.query(Order).filter(Order.id == id, Order.user == current_user).first()
    # orders = current_user.orders
    # for order in orders:
    if order.id == id:
        order_data = {
                'id': order.id,
                'user': {
                    'id': order.user.id,
                    'username': order.user.username,
                    'email': order.user.email,
                    'is_staff': order.user.is_staff,
                    'is_active': order.user.is_active,
                },
                'product': {
                    'id': order.product.id,
                    'name': order.product.name,
                    'price': order.product.price,
                },
                'quantity': order.qty,
                'order_statuses': order.order_status.value,
                'total_price': order.qty * order.product.price,

            }
        return jsonable_encoder(order_data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
    


@order_router.patch('/status-update/{id}/', status_code=status.HTTP_200_OK)
async def updatde_order_status(id: int, order:OrderStatusModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(detail=f'Enter valid access token', status_code=status.HTTP_401_UNAUTHORIZED)
    
    username = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == username).first()
    print('salom', user)
    if user:
        order_to_update = session.query(Order).filter(Order.id == id).first()
        print('order_to_update', order_to_update)
        order_to_update.order_status = order.order_status
        session.commit()
        data = {
            'success': True,
            'code': 200,
            'message': 'User order status updated successfully',
            'data': {
                'id': order_to_update.id,
                'order_status': order_to_update.order_status.value
            }
        }
        return jsonable_encoder(data)
    raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)
