########################################################################################################################
# IMPORTS

import gettext
import logging
import pycountry
from geopy.distance import geodesic

import requests

from ..params.nominatim import POSTCODES

########################################################################################################################
# CLASSES

logger = logging.getLogger(__name__)
spanish = gettext.translation("iso3166-1", pycountry.LOCALES_DIR, languages=["es"])
spanish.install()


class GeoNames:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @staticmethod
    def validate_postcode(postcode):
        if isinstance(postcode, int):
            postcode = str(postcode)

        if postcode and len(postcode) == 5 and postcode[:2] in POSTCODES:
            return postcode

        if postcode and len(postcode) == 4:
            postcode = f"0{postcode}"
            if postcode[:2] in POSTCODES:
                return postcode

    @staticmethod
    def get_province_from_postcode(postcode):
        if postcode:
            return POSTCODES[postcode[:2]]

    def reverse(self, lat, lon):
        return requests.get(f"{self.endpoint}/reverse?lat={lat}&lon={lon}").json()


class Nominatim:
    def __init__(self, nominatim_endpoint, geonames_endpoint):
        self.endpoint = nominatim_endpoint
        self.geonames = GeoNames(geonames_endpoint)

    @staticmethod
    def get_attribute(raw_json, keys):
        for key in keys:
            if key in raw_json:
                return raw_json[key]

    def geocode(self, address):
        return requests.get(f"{self.endpoint}/search?q={address}&format=json").json()

    def geocode_parsed(self, address):
        results = self.geocode(address)

        if results:
            return self.reverse_parsed(results[0]["lat"], results[0]["lon"])

    def reverse(self, lat, lon):
        return requests.get(f"{self.endpoint}/reverse?lat={lat}&lon={lon}&format=json").json()

    def reverse_parsed(self, lat, lon):
        nominatim_raw_json = self.reverse(lat, lon)
        geonames_raw_json = self.geonames.reverse(lat, lon)

        nominatim_res_lat_str = nominatim_raw_json.get("lat")
        nominatim_res_lon_str = nominatim_raw_json.get("lon")
        geonames_res_lat_str = geonames_raw_json.get("lat")
        geonames_res_lon_str = geonames_raw_json.get("lon")

        dist_nominatim = float("inf")
        dist_geonames = float("inf")

        try:
            input_coords = (float(lat), float(lon))
        except (ValueError, TypeError):
            logger.error(f"Invalid input coordinates for distance calculation: lat={lat}, lon={lon}")
        else:
            if nominatim_res_lat_str and nominatim_res_lon_str:
                try:
                    nominatim_coords = (float(nominatim_res_lat_str), float(nominatim_res_lon_str))
                    dist_nominatim = geodesic(input_coords, nominatim_coords).km
                except (ValueError, TypeError):
                    logger.warning("Invalid Nominatim coordinates for distance calculation.")

            if geonames_res_lat_str and geonames_res_lon_str:
                try:
                    geonames_coords = (float(geonames_res_lat_str), float(geonames_res_lon_str))
                    dist_geonames = geodesic(input_coords, geonames_coords).km
                except (ValueError, TypeError):
                    logger.warning("Invalid GeoNames coordinates for distance calculation.")

        if dist_nominatim <= dist_geonames and nominatim_res_lat_str is not None and nominatim_res_lon_str is not None:
            # Use Nominatim data
            raw_address = nominatim_raw_json.get("address", {})
            postcode_str = str(raw_address.get("postcode", ""))
            postcode = self.geonames.validate_postcode(postcode_str)
            province = self.geonames.get_province_from_postcode(postcode) if postcode else None
            city = self.get_attribute(raw_address, ["city", "town", "village"])
            district, quarter = self.get_district_quarter(raw_address)

            return {
                "country": raw_address.get("country"),
                "country_code": (raw_address.get("country_code") or "").lower(),
                "state": raw_address.get("state"),
                "province": province,
                "city": city,
                "postcode": postcode,
                "district": district,
                "quarter": quarter,
                "street": raw_address.get("road"),
                "number": raw_address.get("house_number"),
            }

        elif dist_geonames < dist_nominatim and geonames_res_lat_str is not None and geonames_res_lon_str is not None:
            # Use GeoNames data
            geonames_country_code_str = geonames_raw_json.get("country_code")
            country_name = None
            if geonames_country_code_str:
                try:
                    country_obj = pycountry.countries.get(alpha_2=geonames_country_code_str.upper())
                    if country_obj:
                        country_name = spanish.gettext(country_obj.name)
                except LookupError:
                    logger.warning(f"Country name not found for code: {geonames_country_code_str} using pycountry.")

            postcode_str = str(geonames_raw_json.get("postal_code", ""))
            postcode = self.geonames.validate_postcode(postcode_str)
            province = self.geonames.get_province_from_postcode(postcode) if postcode else None
            city = geonames_raw_json.get("place_name")

            return {
                "country": country_name,
                "country_code": (geonames_country_code_str or "").lower(),
                "state": geonames_raw_json.get("community"),
                "province": province,
                "city": city,
                "postcode": postcode,
                "district": None,
                "quarter": None,
                "street": None,
                "number": None,
            }

        else:
            # Neither source provided valid coordinates
            return {
                "country": None,
                "country_code": None,
                "state": None,
                "province": None,
                "city": None,
                "postcode": None,
                "district": None,
                "quarter": None,
                "street": None,
                "number": None,
            }

    def get_district_quarter(self, raw_json):
        district = self.get_attribute(raw_json, ["city_district", "suburb", "borough"])
        quarter = self.get_attribute(raw_json, ["quarter", "neighbourhood"])

        if not district and quarter:
            district = quarter
            quarter = None

        return district, quarter


class NominatimInterface(Nominatim):
    def __init__(self, config):
        if "osm" in config:
            self.config = config["osm"]

            self.nominatim_endpoint = self.config["nominatim_endpoint"]
            self.geonames_endpoint = self.config["geonames_endpoint"]

            super().__init__(self.nominatim_endpoint, self.geonames_endpoint)
        else:
            logger.warning("no osm section in config")
