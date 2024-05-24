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

@product_router.get('/list/', status_code=status.HTTP_200_OK)
async def get_all_products(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Enter a invalid access token')
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    if current_user:
        products = session.query(Product).all()
        custom_data = [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
            }
            for product in products
        ]
        return jsonable_encoder(custom_data)
    raise HTTPException(detail=f'only Super Admin can  new product add', status_code=status.HTTP_403_FORBIDDEN)

@product_router.get('/{id}/')
async def get_product_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    if current_user:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            custom_order = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
            }
            return jsonable_encoder(custom_order)
        return HTTPException(detail=f'Product not found', status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail=f'only Super Admin is allowed to this request', status_code=status.HTTP_403_FORBIDDEN)



@product_router.delete('/{id}/', status_code=status.HTTP_404_NOT_FOUND)
async def delete_product_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user)
    if current_user:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            session.delete(product)
            session.commit()
            data = {
                'success': True,
                'code': 200,
                'message': 'Product deleted successfully'
            }
            return jsonable_encoder(data)
        raise HTTPException(detail='This is id not found', status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail=f'only Super Admin is product delete', status_code=status.HTTP_403_FORBIDDEN)


@product_router.put('/{id}/')
async def update_product_by_id(id: int, update_product: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    if current_user:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            for key, value in update_product.dict(exclude_unset=True).items():
                setattr(product, key, value)
            session.commit()
            data = {
                'success': True,
                'code': 200,
                'data': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                }
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(detail='Product not found', status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail=f'only Super Admin is allowed to this request', status_code=status.HTTP_403_FORBIDDEN)



@product_router.patch('/{id}/', status_code=status.HTTP_200_OK)
async def patch_product_by_id(id: int, update_product: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(detail=f'Invalid token {str(e)}', status_code=status.HTTP_400_BAD_REQUEST)
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    if current_user:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            for key, value in update_product.dict(exclude_unset=True).items():
                setattr(product, key, value)
            session.commit()
            data = {
                'success': True,
                'code': 200,
                'message': 'Product successfully updated',
                'data': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                }
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(detail='Product not found', status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail=f'only Super Admin is allowed to this request', status_code=status.HTTP_403_FORBIDDEN)