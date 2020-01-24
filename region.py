import json
import re
import additional_function
import item

LAST_REGION_LAYER = 3

class Region(item.Item):

    def _get_region_names(self):
        region_names = []
        try:

            pattern = r"(\|(?:\s|)region\d+name(?s:.)+?)(\n\n)"
            regions = re.findall(pattern, self._dump)

            if len(regions) == 0:
                return region_names

            for region in regions:
                pattern = r"name(?:\s|)=(?:\s|)(.+)"
                name = re.search(pattern, region[0])
                region_names.append(name.group(1))

        except Exception as e:
            additional_function.logs("ID = 1222; Error = " + str(e))

        return  region_names

    def _get_cities_names(self):
        cities_names = []
        try:
            r = re.compile(r"marker\|type=(?P<type>\w+)\|name=(?P<name>[\[\]a-zA-Z\s\|\(\)\-\.]+)(\|url\=(?P<url>(\d|\.|\-|)+))?(\|lat\=(?P<lat>(\d|\.|\-|)+))?(\|long\=(?P<long>(\d|\.|\-|)+))?(\|image\=(?P<image>([\[\]a-zA-Z\s\|\(\)\-\.]|)+))?(\|wikidata\=)?(?P<wikidata>[a-zA-Z0-9]+)?}}")
            cities_names = [m.group("name") for m in r.finditer(self._dump)]
        except Exception as e:
            pass
        return cities_names

    def add_region(self, region):
        self.regions.append(region)



    def add_all_regions(self, full_dump:str, layer_number=0):
        for region_name in self.regions_names:
            r = Region(region_name, full_dump, layer_number)
            self.add_region(r)

    @classmethod
    def init_deep(cls, name: str, full_dump: str, layer_number: int, cities_names=[], regions_names=[]):
        """
        Create region with few layers of region or cities.
        layer_number == number of layer (0,1,2,3)
        deep == how deep should be region
        """
        last_layer_number = LAST_REGION_LAYER
        region = cls(name, full_dump, layer_number=last_layer_number, cities_names=cities_names, regions_names=regions_names)

        for i in range(last_layer_number, layer_number, -1):
            regions = [region]
            region = cls(name, full_dump, layer_number=i-1, regions=regions)

        return region


    def __init__(self, name: str, full_dump: str, layer_number: int, cities_names=[], regions_names=[], regions=[]):
        """

        :param name:+
        :param full_dump:
        :param cities: City object list
        :param regions: Region object list
        """

        super().__init__(name, full_dump)
        self.layer_number = layer_number
        self.regions = []
        self.cities_names = []
        self.regions_names = []
        if name == "Other":
            self.cities_names = cities_names
            self.regions_names = regions_names
            self.regions = regions
        else:

            regions_names = self._get_region_names()
            # first_region_layer_names = self._get_first_region_layer_names()
            self.regions_names = []

            if len(regions_names) == 0:
                cities_names = self._get_cities_names()
                if len(cities_names) == 0 and layer_number < LAST_REGION_LAYER:
                    region = Region.init_deep("Other", full_dump, layer_number + 1, cities_names=[name])
                    self.regions = [region]
                    # self.regions_names.append("Other")

                else:
                    if layer_number < LAST_REGION_LAYER:
                        region = Region.init_deep("Other", full_dump, layer_number + 1, cities_names=cities_names)
                        self.regions = [region]
                    else:
                        self.cities_names = cities_names
                    # self.regions_names.append("Other")

            else:
                self.regions_names = regions_names


