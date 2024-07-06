from sqladmin import ModelView
from .models import Item, Comment, Catalogue
from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        admin_user = 'Utkir'
        admin_password = '090909'

        if admin_user == username and admin_password == password:
            # Validate username/password credentials
            # And update session
            request.session.update({"token": "..."})

            return True

        else:
            return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key="key")

class ItemAdmin(ModelView, model=Item):
    column_list = [Item.id, Item.title, Item.type, Item.price, Item.country,Item.brand, Item.size]


class CommentAdmin(ModelView, model=Comment):
    column_list = [Comment.id,Comment.name, Comment.email, Comment.text]

class CatalogueAdmin(ModelView, model=Catalogue):
    column_list = [Catalogue.id, Catalogue.name]

