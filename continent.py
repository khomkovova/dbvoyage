import additional_function
import re
class Continent():
    def _get_description(self):
        pattern = r"<text.+>.+((?s:.)+?)(==)"
        result = re.search(pattern, self.dump)
        return result.group(1)

    def _get_name(self):
        pattern = r"<title>(.+)</title>"
        result = re.search(pattern, self.dump)
        return result.group(1)

    def _get_id(self):
        pattern = r"<id>(.+)</id>"
        result = re.search(pattern, self.dump)
        return result.group(1)

    def _get_countries_regions(self):
        def region_parse(dump):
            region = {}
            pattern = r"name(?:\s|)=(?:\s|)(.+)"
            result = re.search(pattern, dump)
            region["name"] = result.group(1)
            countries = []

            # if we don't find items, it mean regionname is list of countries in this region. So we create region with name OTHER
            try:
                pattern = r"items=(.+)"
                result = re.search(pattern, dump)
                pattern = r"\[\[.+?\]\]"
                countries_re = re.findall(pattern, result.group(1))
                for country in countries_re:
                    countries.append(additional_function.get_first_name_from_double_meaning_word(country))
                region["countries"] = countries
            except Exception as e:
                pattern = r"\[\[.+?\]\]"
                countries = re.findall(pattern, region["name"])
                region["countries"] = countries
                region["name"] = "Other - {}".format(region["name"])

            pattern = r"description=(.+)"
            result = re.search(pattern, dump)
            region["description"] = result.group(1)

            return region
        pattern = r"(\|(?:\s|)region\d+name(?s:.)+?)(\n\n)"
        regions = re.findall(pattern, self.dump)

        countries_regions = []
        for region in regions:
            parsed_region = region_parse(region[0])
            countries_regions.append(parsed_region)
        return countries_regions
    def __init__(self, name, full_dump):
        self.dump = additional_function.get_one_item(name, full_dump)
        self.description = self._get_description()
        self.name = self._get_name()
        self.id = self._get_id()
        self.countries_regions = self._get_countries_regions()




