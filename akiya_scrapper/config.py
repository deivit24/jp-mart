from pydantic import BaseModel
from decouple import config
from typing import List


class Coords(BaseModel):
    sw_lon: float
    sw_lat: float
    ne_lon: float
    ne_lat: float



class CityCoords(BaseModel):
    city_coords: List[Coords] = []
    city: str = ""
    city_count: int = 0


class JapanLocation(BaseModel):
    name: str
    num: int = 100


SHARED_VOLUME_PATH="/shared/csv_files"

JAPAN_CITIES = [
    # JapanLocation(name="Tokyo"),
    # JapanLocation(name="Yokohama"),
    # JapanLocation(name="Osaka"),
    # JapanLocation(name="Nagoya"),
    # JapanLocation(name="Sapporo"),
    # JapanLocation(name="Kobe"),
    # JapanLocation(name="Fukuoka"),
    # JapanLocation(name="Kyoto"),
    # JapanLocation(name="Kawasaki"),
    # JapanLocation(name="Saitama"),
    # JapanLocation(name="Hiroshima"),
    # JapanLocation(name="Sendai"),
    # JapanLocation(name="Kitakyushu"),
    # JapanLocation(name="Chiba"),
    # JapanLocation(name="Setagaya"),
    # JapanLocation(name="Sakai"),
    # JapanLocation(name="Niigata"),
    # JapanLocation(name="Hamamatsu"),
    # JapanLocation(name="Kumamoto"),
    # JapanLocation(name="Sagamihara"),
    # JapanLocation(name="Nerima"),
    # JapanLocation(name="Shizuoka"),
    # JapanLocation(name="Okayama"),
    # JapanLocation(name="Kagoshima"),
    # JapanLocation(name="Funabashi"),
    # JapanLocation(name="Higashi-Osaka"),
    # JapanLocation(name="Amagasaki"),
    # JapanLocation(name="Hachioji"),
    # JapanLocation(name="Matsudo"),
    # JapanLocation(name="Himeji"),
    # JapanLocation(name="Nagasaki"),
    # JapanLocation(name="Matsuyama"),
    # JapanLocation(name="Kanazawa"),
    # JapanLocation(name="Kawaguchi"),
    # JapanLocation(name="Ichikawa"),
    # JapanLocation(name="Yokosuka"),
    # JapanLocation(name="Nishinomiya"),
    # JapanLocation(name="Utsunomiya"),
    # JapanLocation(name="Urawa"),
    # JapanLocation(name="Kurashiki"),
    # JapanLocation(name="Gifu"),
    # JapanLocation(name="Toyonaka"),
    # JapanLocation(name="Oita"),
    # JapanLocation(name="Omiya"),
    # JapanLocation(name="Wakayama"),
    # JapanLocation(name="Hirakata"),
    # JapanLocation(name="Fukuyama"),
    # JapanLocation(name="Takatsuki"),
    # JapanLocation(name="Asahikawa"),
    # JapanLocation(name="Iwaki"),
    # JapanLocation(name="Fujisawa"),
    # JapanLocation(name="Nara"),
    # JapanLocation(name="Machida"),
    JapanLocation(name="Nagano"),
    # JapanLocation(name="Suita"),
    # JapanLocation(name="Toyohashi"),
    # JapanLocation(name="Toyota"),
    # JapanLocation(name="Takamatsu"),
    # JapanLocation(name="Toyama"),
    # JapanLocation(name="Kochi"),
    # JapanLocation(name="Koriyama"),
    # JapanLocation(name="Hakodate"),
    # JapanLocation(name="Okazaki"),
    # JapanLocation(name="Kashiwa"),
    # JapanLocation(name="Kawagoe"),
    # JapanLocation(name="Naha"),
    # JapanLocation(name="Tokorozawa"),
    # JapanLocation(name="Akita"),
    # JapanLocation(name="Aomori"),
    # JapanLocation(name="Miyazaki"),
    # JapanLocation(name="Maebashi"),
    # JapanLocation(name="Koshigaya"),
    # JapanLocation(name="Yao"),
    # JapanLocation(name="Fukushima"),
    # JapanLocation(name="Yokkaichi"),
    # JapanLocation(name="Akashi"),
    # JapanLocation(name="Kasugai"),
    # JapanLocation(name="Tokushima"),
    # JapanLocation(name="Shimonoseki"),
    # JapanLocation(name="Ichinomiya"),
    # JapanLocation(name="Otsu"),
    # JapanLocation(name="Ichihara"),
    # JapanLocation(name="Neyagawa"),
    # JapanLocation(name="Ibaraki"),
    # JapanLocation(name="Fukui"),
    # JapanLocation(name="Yamagata"),
    # JapanLocation(name="Hiratsuka"),
    # JapanLocation(name="Sasebo"),
    # JapanLocation(name="Shimizu"),
    # JapanLocation(name="Hachinohe"),
    # JapanLocation(name="Kakogawa"),
    # JapanLocation(name="Takasaki"),
    # JapanLocation(name="Morioka"),
    # JapanLocation(name="Mito"),
    # JapanLocation(name="Kurume"),
    # JapanLocation(name="Fuji"),
    # JapanLocation(name="Kure"),
    # JapanLocation(name="Numazu"),
    # JapanLocation(name="Fuchu"),
    # JapanLocation(name="Soka"),
    JapanLocation(name="Kushiro"),
    # JapanLocation(name="Hitachi"),
    # JapanLocation(name="Takarazuka"),
]

class JapanCities(BaseModel):
    cities: List[JapanLocation]

    def city_exists(self, city_name: str) -> bool:
        return any(city.name.lower() == city_name.lower() for city in self.cities)

class AkiyaConfig(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str
    bucket: str
    last_page: int
    chunk_size: int
    secret: str
    listing_attributes: List[str]
    listings_attributes: List[str]
    cities: JapanCities
    email: str
    password: str




LISTINGS_ATTRIBUTES = [
    "listing_id",
    "city",
    "akiya_type",
    "construction_year",
    "gross_yield",
    "is_featured",
    "is_liked",
    "kind",
    "lat",
    "like_count",
    "lon",
    "prefecture",
    "price_foreign",
    "price_yen",
    "translated_address",
    "view_count",
    "image_urls",
]
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

COORDIATE_ATTRIBUTES = ["sw_lon", "sw_lat", "ne_lon", "ne_lat", "city", "city_count"]

akiya_config = AkiyaConfig(
    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    aws_default_region=config("AWS_DEFAULT_REGION"),
    bucket=config("BUCKET"),
    last_page=config("LAST_PAGE"),
    chunk_size=config("CHUNK_SIZE"),
    secret=config("SECRET_KEY"),
    listing_attributes=LISTING_ATTRIBUTES,
    listings_attributes=LISTINGS_ATTRIBUTES,
    cities=JapanCities(cities=JAPAN_CITIES),
    email=config("EMAIL"),
    password=config("PASSWORD"),
)
