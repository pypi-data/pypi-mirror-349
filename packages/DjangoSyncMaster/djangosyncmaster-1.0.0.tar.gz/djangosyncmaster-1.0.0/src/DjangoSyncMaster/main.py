
import logging
from pprint import pprint
from typing import Any

from django.apps import apps, AppConfig

class sync_db:

    def why_bd(self): # Returns the database engine name in use (e.g., mysql, sqlite, etc)
        BDS = ['sqlite', 'postgresql', 'mysql', 'oracle', 'pyodbc', 'sql_server', 'djongo']
        return next((name for name in BDS if name in self.engine), 'unknown')

    def heritage_check(self,modelo): # Checks if the model inherits from Django internal base classes
            nomes = set()
            for base in modelo.__mro__:
                nomes.add(base.__name__)
            return nomes & {
                'AbstractBaseUser',
                'PermissionsMixin',
                'SessionBase',
                'ContentType',
                'LogEntry',
                'BaseUserManager',
                'Permission',
                'Group',
            }

    def map_foreign_keys(self): # Maps all ForeignKeys from app models and their on_delete actions

        from django.db import models

        #* Mapping of ForeignKeys
        foreign_keys_map = {
            'CASCADE': {},
            'SET NULL': {},
            'SET DEFAULT': {},
            'RESTRICT': {},
            'DO NOTHING': {},
            'UNKNOWN': {},
        }

        if self.DEBUG: print('\n')

        for model in apps.get_models():

            if self.DEBUG: print(f'\nModelo: {model}, app_label: "{model._meta.app_label}"')

            # Filters to ignore non-relevant models
            DJANGO_APPS = {'auth', 'contenttypes', 'sessions', 'admin', 'messages', 'staticfiles'}
            if model._meta.app_label in DJANGO_APPS:
                if self.DEBUG: print('-❌DJANGO_APPS❌-')
                continue
            if model._meta.abstract or not model._meta.managed:     # Ignore abstract models and those not managed (managed=False)
                if self.DEBUG: print('-❌abstract or managed❌-')
                continue
            if model._meta.app_label.startswith('django.contrib'):  # Ignore contrib apps, from pure Django
                if self.DEBUG: print('-❌django.contrib❌-')
                continue
            if model._meta.app_label != self.sender.name:           # Ignore Table from outher apps
                if self.DEBUG: print('-❌Not app name❌-') 
                continue
            #if self.heritage_check(model):                         # Ignore heritage tables from Django
            #    if self.DEBUG: print('-❌heritage_check❌-')      
            #    continue

            self.table_to_sync.append(model._meta.db_table)
            if self.DEBUG: print('-✅-')

            table_name = model._meta.db_table
            for field in model._meta.fields:
                if isinstance(field, models.ForeignKey): # Here's the magic: deconstruct to get the original on_delete
                    # Gets the on_delete action for the FK
                    _, _, args, kwargs = field.deconstruct()
                    on_delete_func = kwargs.get("on_delete")
                    if on_delete_func == models.CASCADE:
                        action = 'CASCADE'
                    elif on_delete_func == models.SET_NULL:
                        action = 'SET NULL'
                    elif on_delete_func == models.SET_DEFAULT:
                        action = 'SET DEFAULT'
                    elif on_delete_func == models.RESTRICT:
                        action = 'RESTRICT'
                    elif on_delete_func == models.DO_NOTHING:
                        action = 'DO NOTHING'
                    else:
                        action = 'UNKNOWN'

                    foreign_keys_map[action].setdefault(table_name, []).append(field.column)
        
        return foreign_keys_map

    def __init__(self, 
        sender: AppConfig, # "self" from apps.py.... contains Django infos
        db_settings: dict[str, dict[str, Any]], # Pull from Django, Database infos
        DB: str = 'default', # Database that will be synchronized
        DEFAULT_ON_DELETE_ACTION: str = 'CASCADE', # What to do for default
        LANG: str = 'en', # en or pt-br
        DEBUG: bool = False, # Enable or Disable debug mode
        **kwargs: Any # Pull extra infos
    ):

        # Initializes the sync, sets configs and calls the correct database method
        print('\n')
        print('🔥 DjangoSyncMaster - Start 🔥')

        #* Information Treatment
        try:
            db_data = db_settings[DB]
            if DEBUG: print('\n🔹 DB:', db_data)
        except:
            if DEBUG: print('\n🔹 DB:', db_settings)
            print("\n❌ Invalid selected database")
            return None

        #* Pulls the information that will be used for synchronization
        self.sender = sender
        self.engine = db_data['ENGINE']
        self.DEFAULT_ON_DELETE_ACTION = DEFAULT_ON_DELETE_ACTION

        self.LANG = LANG     # Language of text * DEFAULT=en
        self.DEBUG = DEBUG   # Debug mode (DEV) * DEFAULT=False
        self.extra = kwargs  # captures extras just to make sure

        self.table_to_sync = []
        self.ForeignKeys = self.map_foreign_keys(); print('\n✅ Mapped ForeignKeys\n')

        if DEBUG: print("\n🧬 ForeignKeys Map:", self.ForeignKeys)

        bd = self.why_bd(); 
        if DEBUG: print('\n⚡ Database:', bd)

        if bd == 'mysql':

            db_config = {
                'user': db_data['USER'],
                'password': db_data['PASSWORD'],
                'host': db_data['HOST'],
                'port': int(db_data['PORT']),
                'database': db_data['NAME'],
            }

            self.mysql_sync(self,db_config)

        elif bd == 'unknown':
            print('⚠️ Database not recognized ⚠️\n')

        else:
            print(bd, ' ⚠️ Not supported! ⚠️ \n')        
        
        print('🔥 DjangoSyncMaster - End 🔥')
        print('\n\n')

        return None
    
    class mysql_sync:

        def __init__(self, core, db_config): # Initializes MySQL connection and syncs ForeignKeys
            
            self.core = core
            self.db_config = db_config

            try:
                import mysql.connector
            except:
                print('\n ⚠️ You need Install pip: ⚠️\n    mysql-connector-python==9.3.0')
                return None

            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            fks = self.get_foreign_keys(cursor)

            debug_map = ['success','warning','err']
            run_debug = {
                'success':[],
                'warning':[],
                'err': [],
            }

            print(f"\n⚙️ Syncing start...")
            for constraint, table, column, ref_table, ref_column in fks:
                if table not in core.table_to_sync or ref_table not in self.core.table_to_sync:
                    continue
                back = self.recreate_foreign_key(cursor, table, constraint, column, ref_table, ref_column)
                run_debug[debug_map[(back[0])]].append(back[1])

            conn.commit()
            cursor.close()
            conn.close()

            if (len(run_debug['err']) == 0) and (len(run_debug['warning']) == 0):
                print("\n✅ Sync sucess! ✅")
                if self.core.DEBUG:
                    pprint(run_debug['success'])

            elif (len(run_debug['err']) == 0):
                print("\n✅ All right foreign keys ✅")
                pprint(run_debug['sucess'])
                print("\n")
                
                print("\n⚠️ Warning Mysql ⚠️")
                pprint(run_debug['warning'])

            else:
                print("\n❌ Faltal error Mysql ❌")
                pprint(run_debug)

            print("\n")

            return None
        
        def recreate_foreign_key(self, cursor, table, constraint, column, ref_table, ref_column):
            # Drops and recreates a ForeignKey with the correct ON DELETE action

            on_delete_action = self.get_on_delete_action(table, column)
            if self.core.DEBUG:
                print(f"\n⚙️ Syncing FK `{constraint}` in `{table}` at column `{column}` with ON DELETE {on_delete_action}...")

            try:
                cursor.execute(f"""
                    ALTER TABLE `{table}`
                    DROP FOREIGN KEY `{constraint}`;
                """)
                #print(f"   🔪 DROP `{constraint}` executado com sucesso.")
            except mysql.connector.Error as err:
                print(f"   ⚠️ Error at remove `{constraint}`: {err}")
                return [1,{
                    'fk': constraint,
                    'msg': (f"warning {err}")
                }]

            try:
                cursor.execute(f"""
                    ALTER TABLE `{table}`
                    ADD CONSTRAINT `{constraint}` FOREIGN KEY (`{column}`)
                    REFERENCES `{ref_table}` (`{ref_column}`) ON DELETE {on_delete_action};
                """)
                print(f"   ✅ FK `{constraint}` rebuild with ON DELETE {on_delete_action}.")
                return [0,{
                    'fk': constraint,
                    'msg': (f"rebuild with ON DELETE {on_delete_action}")
                }]
            except mysql.connector.Error as err:
                print(f"   ❌ Error to add `{constraint}`: {err}") 
                return [2,{
                    'fk': constraint,
                    'msg': (f"Error {err}")
                }]  
            

        def get_on_delete_action(self, table, column):
            # Search for the correct action for this FK in the dictionary, otherwise return (DEFAULT_ON_DELETE_ACTION or CASCADE)
            if self.core.DEBUG:
                print(f"\n🧪 Procurando por Tabela='{table}' e Coluna='{column}'")
            for action, tables in self.core.ForeignKeys.items():
                if self.core.DEBUG: print(f"🔸 Testing action: {action}")
                cols = tables.get(table)
                if cols and column in cols:
                    return action
            return self.core.DEFAULT_ON_DELETE_ACTION

        def get_foreign_keys(self,cursor):
            # Gets all ForeignKeys from the MySQL database
            query = """
                SELECT
                    rc.CONSTRAINT_NAME,
                    rc.TABLE_NAME,
                    kcu.COLUMN_NAME,
                    kcu.REFERENCED_TABLE_NAME,
                    kcu.REFERENCED_COLUMN_NAME
                FROM information_schema.REFERENTIAL_CONSTRAINTS rc
                JOIN information_schema.KEY_COLUMN_USAGE kcu
                    ON rc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
                    AND rc.CONSTRAINT_SCHEMA = kcu.CONSTRAINT_SCHEMA
                WHERE rc.CONSTRAINT_SCHEMA = %s;
            """
            cursor.execute(query, (self.db_config['database'],))
            return cursor.fetchall()



