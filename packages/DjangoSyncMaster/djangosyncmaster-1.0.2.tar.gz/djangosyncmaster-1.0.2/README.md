
# DjangoSyncMaster

## Description

**Powerful tool for truly synchronizing data and its relationships in database tables.**
- Truly maps Foreign Keys and their on_delete rules in Django.

Django uses a migration system based on ORM (Object-Relational Mapping) to make changes to the database, However, this can become problematic when using Foreign Keys, since Django does not implement ON DELETE when synchronizing the database... This can be problematic if you want to change the data directly in the database.

This library aims to bring this automation to Django. When you perform a migration, the script will automatically read the tables created in models.py (ignoring any table that has not been declared outside of your app's models.py, this includes third-party tables and Django's own standards).

As soon as it performs a reading and separates the tables that were actually declared manually in models.py, it will create a map of your Foreign Keys and recreate them manually, one by one. With the configuration defined in your models.py.

This library aims to bring speed and automation to the development environment. (Not recommended for implementation environments)

This way, you won't need to edit a migration directly or modify the database by hand.

**obs**: I am not responsible for any type of data loss, as previously stated, this library aims to streamline the development environment and not to manage the implemented project.

## How to use

1. Install the package using pip:

```bash

pip install DjangoSyncMaster

```

2. Add 'DjangoSyncMaster' to your Django app's apps.py file:

```python

from django.apps import AppConfig
from django.conf import settings

from DjangoSyncMaster import sync_db

class AppNameConfig(AppConfig):
	name = 'app_Name'

	def ready(self):
		from django.db.models.signals import post_migrate # await migrate

	def handler(sender, **kwargs): # for pull Django instance info
		sync_db(sender,db_settings=settings.DATABASES)

  post_migrate.connect(handler, sender=self) #Execute function pos-migrate

```
3. Make migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

