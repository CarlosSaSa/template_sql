import json
import sys
import random

# Diccionario para los tipos de datos
dict_datatypes = {
    "int": "INT",
    "date": "DATE",
    "float": "FLOAT",
    "required": "NOT NULL",
    "string": "VARCHAR",
    "bool": "BOOLEAN"
}

# Función para crear la plantilla
def createtTemplate( name: str, columns: list[str] ):

    # Obtenemos el ultimo elemento y le tenemos que quitar el punto y coma si existe
    size = len(columns) - 1
    column_temp = []
    for index, value in enumerate( columns ):
        if index > 0 and index == size:
            # Tenemos que quitar el punto y coma de la cadena
            value_tmp = "\t" + value.replace(';', '')
            column_temp.append( value_tmp )
        elif index > 0:
            value_tmp = "\t" + value
            column_temp.append( value_tmp )
        else:
             column_temp.append( value )

    format_column = "\n".join( column_temp )
    sql = f"CREATE TABLE { name } ( \n\t{ format_column } ); \n\n"

    return sql

# Función para crear la columna
def createColumnSql( column_name: str, column_datatype: str, required: str, primaryKey:str = '' ):
    return f"{column_name} { column_datatype } { required }{ ' ' + primaryKey if primaryKey else '' };"

# Función para crear una fk 
def createFksColumns( table_name: str, meta_data: dict ):
    # Obtenemos algunos valores de los metadatos
    if not meta_data.get('isFk'):
        return
    if meta_data.get('isFk') and 'dependsOn' not in meta_data:
        sys.exit('Debe de contener la tabla padre')
    

    random_number = random.randint( 999, 99999 )
    constraint_name = f"{ meta_data.get('dependsOn') }_{ meta_data.get('name') }_{random_number}"
    return f"ALTER TABLE { table_name } ADD CONSTRAINT {constraint_name} FOREIGN KEY ({ meta_data.get('name') }) REFERENCES { meta_data.get('dependsOn') }( { meta_data.get('name') } ); \n"

# Función para dar formato a la columna
def formatColumn( meta_data: dict ):
  
    # Obtenemos algunos datos
    column_name = meta_data.get('name')
    data_type = dict_datatypes.get(meta_data.get('type'), 'INT')
    maxlenth = meta_data.get('maxlength')
    required =  'NOT NULL' if meta_data.get('required') else ''
    primaryKey = 'PRIMARY KEY' if meta_data.get('primaryKey') else ''
    isIdentity = meta_data.get('identity', False)

    # Si el tipo de dato es varchar y hay un maxlength entonces volvemos a formatear la cadena
    if data_type == 'VARCHAR' and maxlenth:
        data_type = f'VARCHAR({maxlenth})'
    
    # Si el tipo de dato es identity
    if isIdentity:
        data_type = f"{data_type} GENERATED ALWAYS AS IDENTITY"

    return createColumnSql( column_name = column_name, column_datatype = data_type, required = required, primaryKey = primaryKey )

# Lista de items de prueba
lista_auditoria = ['created_at TIMESTAMP NOT NULL DEFAULT now();', 'updated_at TIMESTAMP NOT NULL;']

file = None
file_sql = None
try:
    file_sql = open('./tables.sql', 'w')
    file = open('./tables.json', 'r', encoding='utf8')
    json_data = json.load( file )
    # Si no existe la clave de tables entonces es un error
    if 'tables' not in json_data:
        sys.exit('No existe la clave tables...')
    # Obtenemos la clave de tables
    tables = json_data.get('tables')        
    tmp_list = [] # Para agregar elementos temporales
    for i in tables:
        table_name = i.get('name')
        columns = i.get('columns')
        column_list = [ formatColumn(j) for j in columns ]
        if i.get('audit', False):
            column_list.extend( lista_auditoria )
        template = createtTemplate( name = table_name, columns = column_list )
        file_sql.write( template )
        # Volvemos a recorrer la lista de columnas para obtener las fk
        columns_fk = [ createFksColumns( table_name, j) for j in columns if j.get('isFk') ]
        file_sql.write( "".join( columns_fk ) )

except FileNotFoundError as e:
    print('No se ha encontrado el archivo para lectura: ', e, type(e))

except Exception as e:
    print('Ha ocurrido la siguiente excepcion: ', e, type(e))
finally:
    if file:
        file.close()
    if file_sql:
        file_sql.close()





