from typing import List

from fastapi import APIRouter, HTTPException

from app.models.tarifa_model import TarifaModel
from app.services import tarifas_service

router = APIRouter(prefix="/tarifas", tags=["Tarifas"])


@router.get("/", response_model=List[TarifaModel])
async def obtener_tarifas():
    """Obtiene todas las tarifas desde MongoDB."""
    return await tarifas_service.get_all_tarifas()


@router.get("/{codigo_ruta}/resumen")
async def obtener_resumen(codigo_ruta: str, anno: int = 2024):
    """Tarifas vigentes y promedio de pasajeros por ramal en el año indicado."""
    resumen = await tarifas_service.get_resumen_ruta(codigo_ruta, anno)
    if not resumen:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return resumen


@router.get("/{codigo_ruta}", response_model=List[TarifaModel])
async def obtener_tarifas_por_ruta(codigo_ruta: str):
    """Obtiene las tarifas vigentes de una ruta."""
    tarifas = await tarifas_service.get_tarifas_vigentes(codigo_ruta)
    if not tarifas:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return tarifas