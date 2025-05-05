from fastapi.responses import JSONResponse
#import pydantic
import pymysql
import pymysql.cursors
from db.bd_mysql import get_db_connetion
from models.user_model import User

class UserService:
    
    def __init__(self):
        
        self.con= get_db_connetion()
        if self.con is None:
            print("No se pudo conectar")
            
            
    async def get_users(self):
        try:
            
            self.con.ping(reconnect=True)
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM usuario")
                users=cursor.fetchall()# esto para cuando hay varios registros
                
                return JSONResponse(
                    status_code=200,
                    content={
                        "sucses": True,
                        "message":"usuarios encontrados con exito",
                        "data":users if users else[]                
                    } 
                )
        except Exception as e: 
             print("Error en get_users:", str(e)) 
             return JSONResponse(
                    status_code=500,
                    content={
                        "sucses": False,
                        "message":f"usuarios  no encontrados {str(e)}",
                        "data": None                
                    } 
                )
             
    async def get_user_by_id(self, user_id: int):      
        
        try:
            self.con.ping(reconnect=True) # reconecto la aplicacion
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
             sql="SELECT * FROM usuario WHERE id= %s"
             cursor.execute(sql,{user_id})
            user=cursor.fetchone # este devuelev un solo dato
            
            if user:
                return JSONResponse(
                    status_code=200,
                    content={
                        "succes": True,
                        "message": "usuario encontrado",
                        "data": user
                    }
                )
            else:   
                return JSONResponse(
                    status_code=404,
                    content={
                        "succes": False,
                        "message": "usuario no encontrado",
                        "data": None
                    }
                ) 
                                   
        except Exception as e: 
            return JSONResponse(
                    status_code=500,
                    content={
                        "succes": False,
                        "message": f"Error al consultar al usuario: {str(e)}",
                        "data": None
                    }
                )
        finally:
            self.con.close() # cierro la conexion 
             
    async def create_user(self,user_data:User):
        try:
             self.con.ping(reconnect=True) # reconecto la aplicacion
             with self.con.cursor() as cursor:
                 check_sql="SELECT COUNT(*) FROM usuario WHERE correo= %s"
                 cursor.execute(check_sql,{user_data.correo})
             result= cursor.fetchone()
             
             if result[0] > 0: 
                 return JSONResponse(
                    status_code=404,
                    content={
                        "succes": False,
                        "message": "El correo ya se encuentra registrado",
                        "data": None
                    }
                ) 
                 
             sql= "INSERT INTO usuario(nombre, apellido, correo, telefono, password, estado) VALUES (%s, %s, %s, %s, %s, %s)"
             cursor.execute(sql,(user_data.nombre, user_data.apellido, user_data.correo, user_data.numtelefono, user_data.password,user_data.estado))
             
             if cursor.lastrowid:
                 return JSONResponse(
                    status_code=201,
                    content={
                        "succes": True,
                        "message": "usuario creado con exito",
                        "data": {"user.id": cursor.lastrowid}
                    }
                )
             else:
                   return JSONResponse(
                    status_code=400,
                    content={
                        "succes": False,
                        "message": "No se pudo resgistrar el usuario",
                        "data": None
                    }
                )      
                     
                      
        except Exception as e: 
             self.con.rollback()
             return JSONResponse(
                    status_code=500,
                    content={
                        "succes": False,
                        "message": f"Error al registrar al usuario: {str(e)}",
                        "data": None
                    }
                )
        finally:
            self.con.close() # cierro la conexion 
            
    async def change_password(self, user_id: int, new_password: str):
    
       try:
            self.con.ping(reconnect=True) # reconecto la aplicacion
            with self.con.cursor() as cursor:
                #verficar que usuario existe
                check_sql= "SELECT COUNT(*) FROM usario WHERE id=%s"
                cursor.execute(check_sql,{user_id})
                result= cursor.fetchone()
                
                if result[0] == 0:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)
                # actualizar contraseña
                sql="UPDATE usuario SET password=%s WHERE id=%s"
                cursor.execute(sql,{new_password, user_id})
                self.con.commit() # Confirmar la transacción
                
                if cursor.rowcount > 0:
                    return  JSONResponse(content={"success": True, "message": "Contraseña actualizada exitosamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=409)
            
                
       except Exception as e: 
           self.con.rollback() # Deshacer la transacción
           return JSONResponse(content={"success": False, "message": f"Error al actualizar la contraseña: {str(e)}"}, status_code=500)
                 
       finally:
           self.con.close() # cierro la conexion       
           
           
           

    async def inactivate_user(self, user_id: int):
        """Inactiva un usuario cambiando su estado a 0 y retorna JSONResponse."""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Verificar si el usuario existe
                check_sql = "SELECT COUNT(*) FROM usuario WHERE id=%s"
                cursor.execute(check_sql, (user_id,))
                result = cursor.fetchone()
                
                if result[0] == 0:  # Si el usuario no existe
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                # Inactivar usuario
                sql = "UPDATE usuario SET estado=0 WHERE id=%s"
                cursor.execute(sql, (user_id,))
                self.con.commit()  

                if cursor.rowcount > 0:
                    return JSONResponse(content={"success": True, "message": "Usuario inactivado exitosamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=400)
        except Exception as e:
            self.con.rollback()  
            return JSONResponse(content={"success": False, "message": f"Error al inactivar usuario: {str(e)}"}, status_code=500)
        finally:
            self.close_connection()
            
            
    async def toggle_user_status(self, user_id: int):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Obtener estado actual
                get_estado_sql = "SELECT estado FROM usuario WHERE id=%s"
                cursor.execute(get_estado_sql, (user_id,))
                result = cursor.fetchone()

                if not result:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                estado_actual = result[0]
                nuevo_estado = 0 if estado_actual == 1 else 1

                update_sql = "UPDATE usuario SET estado=%s WHERE id=%s"
                cursor.execute(update_sql, (nuevo_estado, user_id))
                self.con.commit()

                return JSONResponse(content={"success": True, "message": "Estado actualizado correctamente."}, status_code=200)
        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al cambiar estado: {str(e)}"}, status_code=500)
        finally:
            self.close_connection()
    
    async def update_user(self, user_id: int, user_data: User):
        """
        Actualiza los datos de un usuario excepto el campo 'estado'.
        """
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Verificar si el usuario existe
                check_sql = "SELECT COUNT(*) FROM usuario WHERE id=%s"
                cursor.execute(check_sql, (user_id,))
                result = cursor.fetchone()

                if result[0] == 0:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                # Actualizar campos (excepto estado)
                update_sql = """
                    UPDATE usuario
                    SET nombre=%s, apellido=%s, correo=%s, numtelefono=%s, password=%s,
                    WHERE id=%s
                """
                cursor.execute(update_sql, (
                    user_data.nombre,
                    user_data.apellido,
                    user_data.correo,
                    user_data.numtelefono,
                    user_data.password,
                    user_id
                ))
                self.con.commit()

                if cursor.rowcount > 0:
                    return JSONResponse(content={"success": True, "message": "Usuario actualizado correctamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=409)

        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al actualizar usuario: {str(e)}"}, status_code=500)
        finally:
            self.close_connection()


    def close_connection(self):
        """Llama al cierre de conexión de la base de datos."""
        self.con.close()    
                
    
        
       
            
            
             
            
                              
                