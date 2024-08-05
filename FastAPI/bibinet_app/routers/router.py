import json
from fastapi import APIRouter, HTTPException
from schemas.part import SearchPartRequest
from database import get_database_connection

router = APIRouter(
    prefix="/search",
)


@router.post("/part/", response_model=dict)
async def search_part(request: SearchPartRequest):
    conn = await get_database_connection()

    query = """
        SELECT
            spm.id AS mark_id,
            spm.name AS mark_name,
            spm.producer_country_name,
            spm2.id AS model_id,
            spm2.name AS model_name,
            spp.name AS part_name,
            spp.price,
            spp.json_data
        FROM spare_parts_part spp
        JOIN spare_parts_part_mark sppm ON spp.id = sppm.part_id
        JOIN spare_parts_mark spm ON sppm.mark_id = spm.id
        JOIN spare_parts_part_model sppp ON spp.id = sppp.part_id
        JOIN spare_parts_model spm2 ON sppp.model_id = spm2.id
        WHERE spp.is_visible = true AND spm.is_visible = true AND spm2.is_visible = true
    """

    conditions = []

    if request.mark_name:
        conditions.append(f"LOWER(spm.name) LIKE LOWER('%{request.mark_name}%')")

    if request.mark_list:
        conditions.append(f"spm.id IN ({','.join(map(str, request.mark_list))})")

    if request.part_name:
        conditions.append(f"LOWER(spp.name) LIKE LOWER('%{request.part_name}%')")

    if request.params.get("is_new_part") is not None:
        conditions.append(f"spp.json_data->>'is_new_part' = '{str(request.params['is_new_part']).lower()}'")

    if request.params.get("color"):
        conditions.append(f"LOWER(spp.json_data->>'color') = LOWER('{request.params['color']}')")

    if request.price_gte is not None:
        conditions.append(f"spp.price >= {request.price_gte}")

    if request.price_lte is not None:
        conditions.append(f"spp.price <= {request.price_lte}")

    if conditions:
        query += " AND " + " AND ".join(conditions)

    offset = (request.page - 1) * 10
    query += f" LIMIT 10 OFFSET {offset}"

    try:
        rows = await conn.fetch(query)

        response = []
        total_price_sum = 0

        for row in rows:
            json_data = json.loads(row['json_data'])
            part_response = {
                "mark": {
                    "id": row['mark_id'],
                    "name": row['mark_name'],
                    "producer_country_name": row['producer_country_name']
                },
                "model": {
                    "id": row['model_id'],
                    "name": row['model_name']
                },
                "name": row['part_name'],
                "json_data": json_data,
                "price": row['price']
            }
            response.append(part_response)
            total_price_sum += row['price']

        return {
            "response": response,
            "count": len(response),
            "summ": total_price_sum
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        await conn.close()
