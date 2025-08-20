import enum 

class Tarea:
    def __init__(self, id, nombre, descripcion, estado, fechaInicio):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado
        self.fechaInicio = fechaInicio

    def ActualizarEstado(self, nuevoEstado):
        self.estado = nuevoEstado

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fechaInicio": str(self.fechaInicio)            
        }

    def from_dict(cls, data):
        return cls(data["id"], data["nombre"], data["descripcion"], data["estado"], data["fechaInicio"])