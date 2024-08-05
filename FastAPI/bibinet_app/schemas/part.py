from pydantic import BaseModel
from typing import List, Optional, Dict


class SearchPartRequest(BaseModel):
    mark_name: Optional[str] = None
    mark_list: Optional[List[int]] = None
    part_name: Optional[str] = None
    params: Optional[Dict] = {}
    price_gte: Optional[float] = None
    price_lte: Optional[float] = None
    page: int = 1


class PartResponse(BaseModel):
    mark: dict
    model: dict
    name: str
    json_data: dict
    price: float
