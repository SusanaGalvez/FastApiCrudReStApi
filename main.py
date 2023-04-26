from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
#Este paquete es para que el id sea único
from uuid import uuid4 as uuid


app=FastAPI()
publicaciones =[]

#Clase de Post Model
class Publicacion(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool=False



@app.get('/')
def read_root():
    return{"welcome":"Welcome to my API"}

#LISTA TODAS LAS PUBLICACIONES
@app.get('/listarTodasPublicaciones')
def listar_todas_publicaciones():
    return publicaciones


#AÑADE UNA PUBLICACIÓN
@app.post('/añadirPublicacion')
def anadir_publicacion(publicacion:Publicacion):
    #CON EL .DICT , LO CONVERTIMOS EN DICCIONARIO, COMO EL JSON DE JS
    #print(post.dict())
    #EN LINEA LE APLICAMOS LO DEL ID UNICO
    publicacion.id=str(uuid())
    # CON ESTA LINEA LE AÑADIMOS A LA LISTA DE PUBLICACIONES
    publicaciones.append(publicacion.dict())
    return publicaciones[-1]

#CONSIGUE UNA PUBLICACIÓN
@app.get('/conseguirPublicacion/{publicacion_id}')
def conseguir_publicacion(publicacion_id:str):
    for publi in publicaciones:
        if publi["id"] == publicacion_id:
            return publi
    raise HTTPException(status_code=404,detail="Publicación  no encontrada")


#BORRA UNA PUBLICACIÓN
@app.delete('/borrarPublicacion/{publicacion_id}')
def borrar_publicacion(publicacion_id:str):
    #Con este for y enumerate nos da la publicación y e indice
    for index, publi  in enumerate(publicaciones):
        if publi["id"]==publicacion_id:
            publicaciones.pop(index)
            return{"message:" "La Publicación ha sido eliminada"}
        raise HTTPException(status_code=404,detail="Publicación  no encontrada")


#MODIFICAR UNA PUBLICACIÓN
@app.put('/modificarPublicacion/{publicacion_id}')
def modificar_publicacion(publicacion_id:str,publicacion_actualizada:Publicacion):
    #Con este for y enumerate nos da la publicación y e indice
    for index, publi  in enumerate(publicaciones):
        if publi["id"]==publicacion_id:
            publicaciones[index]["title"] = publicacion_actualizada.title
            publicaciones[index]["content"] = publicacion_actualizada.content
            publicaciones[index]["author"] = publicacion_actualizada.author
            return{"message:" "La Publicación ha sido modificada"}
        raise HTTPException(status_code=404,detail="Publicación  no encontrada")

