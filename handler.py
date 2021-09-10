import json
import pymysql


def password_check(passwd):
      
    SpecialSym =['$', '@', '#', '%', '*']
    val = True
      
    if len(passwd) < 6:
        print('length should be at least 6')
        val = False
          
    if len(passwd) > 20:
        print('length should be not be greater than 8')
        val = False
          
    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        val = False
          
    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False
          
    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        val = False
          
    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')
        val = False
    
    return val

def crearUsuario (event, context):
    usuario = json.loads(event['body'])['usuario']
    p4ss = json.loads(event['body'])['pass']

    if usuario == '' or p4ss == '' :
            response = {
                "statusCode": 500,
                "body": json.dumps({
                    "codigo":500,
                    "descripcion": "Credenciales Incorrectas!!"
                })
            }
            return response

    if password_check(p4ss) == False:
        response = {
            "statusCode": 500,
            "body": json.dumps({
                "codigo":500,
                "descripcion": "No cumple con politicas de contraseña!!"
            })
        }
        return response

    connection = pymysql.connect(host='localhost',
                            user='root',
                            password='',
                            database='python',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `usuarios` (`usuario`, `pass`) VALUES (%s, %s)"
            cursor.execute(sql, (usuario, p4ss))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()


    response = {
            "statusCode": 200,
            "body": json.dumps({
                "codigo":200,
                "descripcion": "Usuario Creado!!"
            })
        }
    return response

  

def login(event, context):

    print('Hola')
    usuario = json.loads(event['body'])['usuario']
    p4ss = json.loads(event['body'])['pass']

    ##Validar que envie un json

    if usuario == '' or p4ss == '' :
        response = {
            "statusCode": 500,
            "body": json.dumps({
                "codigo":500,
                "descripcion": "Credenciales Incorrectas!!"
            })
        }
        return response

    if password_check(p4ss) == False:
        response = {
            "statusCode": 500,
            "body": json.dumps({
                "codigo":500,
                "descripcion": "No cumple con politicas de contraseña!!"
            })
        }
        return response

    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='python',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



    with connection:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT id, usuario, pass FROM `usuarios` WHERE `usuario`=%s and pass=%s"
            cursor.execute(sql, (usuario,p4ss))
            result = cursor.fetchone()
            if bool(result):
                response = {
                    "statusCode": 200,
                    "body": json.dumps({
                        "codigo":200,
                        "descripcion": "usuario encontrado",
                        "usuario": result
                    })
                }
                return response    
            else :
                response = {
                    "statusCode": 404,
                    "body": json.dumps({
                        "codigo":404,
                        "descripcion": "usuario NO encontrado",
                    })
                }
                return response  



    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
