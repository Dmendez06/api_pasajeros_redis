from typing import List

from app.cache.redis import redis_cache
from app.config import settings
from app.db.mongo import db


@redis_cache(ttl_seconds=settings.redis_ttl)
async def get_all_tarifas() -> List[dict]:
    return await db.tarifas.find().to_list()


async def get_tarifas_vigentes(codigo_ruta: str) -> List[dict]:
    ultima = await db.tarifas.find_one(
        {"codigo_ruta": codigo_ruta},
        sort=[("fecha_vigencia", -1)],
    )
    if not ultima:
        return []
    return await db.tarifas.find(
        {"codigo_ruta": codigo_ruta, "fecha_vigencia": ultima["fecha_vigencia"]}
    ).to_list()


@redis_cache(ttl_seconds=settings.redis_ttl)
async def get_resumen_ruta(codigo_ruta: str, anno: int) -> dict:
    tarifas = await get_tarifas_vigentes(codigo_ruta)
    if not tarifas:
        return {}

    pipeline = [
        {"$match": {"codigo_ruta": codigo_ruta, "anno": anno}},
        {
            "$group": {
                "_id": "$codigo_ramal",
                "promedio": {
                    "$avg": {
                        "$add": [
                            {"$ifNull": ["$pasajeros_regulares", 0]},
                            {"$ifNull": ["$pasajeros_adulto_mayor", 0]},
                        ]
                    }
                },
            }
        },
    ]
    ramales = await (await db.passengers.aggregate(pipeline)).to_list()

    promedio = (
        sum(r["promedio"] for r in ramales) / len(ramales) if ramales else 0.0
    )

    return {
        "codigo_ruta": codigo_ruta,
        "nombre_ruta": tarifas[0]["nombre_ruta"],
        "anno_pasajeros": anno,
        "tarifas_vigentes": [
            {
                "nombre_fraccionamiento": t["nombre_fraccionamiento"],
                "tarifa_regular": t["tarifa_regular"],
                "tarifa_adulto_mayor": t["tarifa_adulto_mayor"],
                "fecha_vigencia": t["fecha_vigencia"],
            }
            for t in tarifas
        ],
        "ramales_considerados": len(ramales),
        "promedio_pasajeros": round(promedio, 1),
    }