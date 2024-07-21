from pydantic import BaseModel
from decouple import config
from typing import List


class AkiyaConfig(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str
    bucket: str
    last_page: int
    chunk_size: int
    secret: str
    listing_attributes: List[str]


LISTING_ATTRIBUTES = [
    "address",
    "building_area",
    "construction_year",
    "description",
    "first_seen_at",
    "gross_yield",
    "has_free_parking",
    "image_urls",
    "is_condo",
    "is_geocoded",
    "is_hidden",
    "is_liked",
    "is_toushi",
    "land_area",
    "last_seen_at",
    "lat",
    "like_count",
    "listing_id",
    "llm_area",
    "llm_description",
    "lon",
    "management_fee_foreign",
    "management_fee_yen",
    "needs_update",
    "prefecture",
    "price_foreign",
    "price_yen",
    "remarks",
    "repair_fee_foreign",
    "repair_fee_yen",
    "station_distance",
    "station_lat",
    "station_lon",
    "station_name",
    "translated_address",
    "translated_condition",
    "translated_description",
    "translated_remarks",
    "url",
]

akiya_config = AkiyaConfig(
    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    aws_default_region=config("AWS_DEFAULT_REGION"),
    bucket=config("BUCKET"),
    last_page=config("LAST_PAGE"),
    chunk_size=config("CHUNK_SIZE"),
    secret=config("SECRET_KEY"),
    listing_attributes=LISTING_ATTRIBUTES,
)
