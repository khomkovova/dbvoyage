import json
import re
import additional_function
import region
import item
class Country(item.Item):
    def _get_first_layer_regions_names(self):
        first_layer_regions_names = []
        try:

            pattern = r"(\|(?:\s|)region\d+name(?s:.)+?)(\n\n)"
            regions = re.findall(pattern, self._dump)

            if len(regions) == 0:
                return  first_layer_regions_names

            for region in regions:
                pattern = r"name(?:\s|)=(?:\s|)(.+)"
                name = re.search(pattern, region[0])
                first_layer_regions_names.append(name.group(1))

        except Exception as e:
            additional_function.logs("ID = 1222; Error = " + str(e))
        return  first_layer_regions_names

    def _get_cities_names(self):
        cities_names = []
        try:
            r = re.compile(r"marker\|type=(?P<type>\w+)\|name=(?P<name>[\[\]a-zA-Z\s]+)(\|lat\=(?P<lat>(\d|\.)+))?(\|long\=(?P<long>(\d|\.)+))?\|wikidata\=(?P<wikidata>[a-zA-Z0-9]+)")
            cities_names = [m.group("name") for m in r.finditer(self._dump)]
        except Exception as e:
            pass
        return cities_names


    def add_first_region_layer(self, first_region_layer):
        self.first_layer_regions.append(first_region_layer)

    def add_all_regions(self, full_dump:str):
        for region_name in self.first_layer_regions_names:
            r = region.Region(region_name, full_dump, 0)
            self.add_first_region_layer(r)




    def __init__(self, name: str, full_dump: str):
        super().__init__(name, full_dump)
        first_layer_regions_names = self._get_first_layer_regions_names()
        self.first_layer_regions_names = []
        self.first_layer_regions = []

        if len(first_layer_regions_names) == 0:
            cities_names = self._get_cities_names()
            if len(cities_names) == 0:
                first_layer_region = region.Region.init_deep("Other", full_dump, 0, cities_names=[name])
                self.add_first_region_layer(first_layer_region)
                # self.first_layer_regions_names.append("Other")

            else:
                first_layer_region = region.Region.init_deep("Other", full_dump, 0, cities_names=cities_names)
                self.add_first_region_layer(first_layer_region)
                # self.first_layer_regions_names.append("Other")
        else:
            self.first_layer_regions_names = first_layer_regions_names




