from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

ObjectIdStr = Annotated[str, BeforeValidator(str)]


class TarifaModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[ObjectIdStr] = Field(default=None, alias="_id")
    codigo_ruta: str
    nombre_ruta: str
    nombre_fraccionamiento: str
    km_por_viaje: float
    tarifa_regular: float
    tarifa_adulto_mayor: float
    resolucion: str
    fecha_resolucion: datetime
    gaceta: int
    alcance: int
    fecha_gaceta: datetime
    fecha_vigencia: datetime
    expediente: str
    operadores: str
    cedulas: str