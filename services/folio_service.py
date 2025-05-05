from typing import Optional, List
from fastapi.responses import JSONResponse
import pymysql
#import pymysql.cursors
from db.bd_mysql import get_db_connetion


class FolioService:
    def __init__(self):
        self.con = get_db_connetion()
        if self. con is None:
            raise Exception( "No se puede conectar a la BD")
           # print("No se pudo conectar")
            
    async def get_folios(self):
        """inicia la conexión"""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql= """SELECT f.id, f.caso, u.monbre, u.apellido,u.numtelefono FROM folio f JOIN usuraio u ON f. usuraio_FK=u.id"""
                
                cursor.execute(sql)
                folio = cursor.fetchall()
                
                if folio:
                    return JSONResponse(content={
                        "succes": True,
                        "data": folio,
                        "message": "Registros encontrados",
                        "status_code":200,
                    } )
                else:
                    return JSONResponse(content={
                        "succes": False,
                        "message": "Folios no encontrados",
                        "status_code":400,
                    }                          
                )   
        except Exception as e:
            return JSONResponse(content={
                        "succes": False,
                        "message": f"Se produjo un error al buscar los folios: {str(e)} ", 
                        "status_code":500,
                    })
        finally:
             self.con.close() # cierro la conexion 
            
    async def get_folio(self, user_id: int):
     try:
            self.con.ping(reconnect=True)
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql= "SELECT f.id, f.caso, u.monbre, u.apellido,u.numtelefono FROM folio f JOIN usuraio u ON f. usuraio_FK=u.id WHERE f.id=%s"
                
                cursor.execute(sql,(user_id),)
                folio = cursor.fetchone()
                
                if folio:
                    return JSONResponse(content={
                        "succes": True,
                        "data": folio,
                        "message": "Registro encontrado",
                        "status_code":200,
                    } )
                else:
                    return JSONResponse(content={
                        "succes": False,
                        "message": "Folio no encontrado",
                        "status_code":400,
                    }                          
                )   
     except Exception as e:
            return JSONResponse(content={
                        "succes": False,
                        "message": f"Problemas al realizar la consulta: {str(e)} ", 
                        "status_code":500,
                    })
     finally:
         self.con.close() # cierro la conexion 
          
    async def create_folio(self, folio_data):
        try:
                self.con.ping(reconnect=True)  
                with self.con.cursor() as cursor:
                 sql= "INSERT INTO FOLIO (nombre, apellido, numcaso, numtelefono, usuario_FK) VALUES {%s, %s, %s, %s, %s}"
                
                cursor.execute(sql,(folio_data.nombre, folio_data.apellido, folio_data.numcaso, folio_data.numtelefono, folio_data.usuario_FK))
                self.con.commit()
                
                if cursor.lastrowid:
                    return JSONResponse(content={
                        "succes": True,
                        "data": cursor.lastrowid,
                        "message": "Folio creado exitosamente",
                        "status_code":200,
                    } )
                else:
                     return JSONResponse(content={
                        "succes": False,
                        "message": "No se pudo crear el folio",
                        "status_code":400,
                    } ) 
        except Exception as e:
            return JSONResponse(content={
                        "succes": False,
                        "message": f"Se produjo al insertar el registro: {str(e)} ", 
                        "status_code":500,
                    })
    def close_connection(self):
            if self.con:  # cierro la conexion 
                self.con.close()               
                                           
                 
                    
                
                   
                     
                    
            
                      
            
           
                
            
    
    