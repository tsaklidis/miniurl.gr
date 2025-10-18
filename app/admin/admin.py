from sqladmin import ModelView

from app.databases.models import Urls, User


class UrlsAdmin(ModelView, model=Urls):
    column_list = [Urls.alias, Urls.original_url, Urls.created_at, Urls.total_clicks]

# class UserAdmin(ModelView, model=User):
#     column_list = [User.username, User.email, User.disabled, User.is_admin]
