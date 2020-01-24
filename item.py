import additional_function
import re
import countries_region
import json
class Item():




    # def _get_name(self) -> str:
    #
    #     pattern = r"<title>(.+)</title>"
    #     result = re.search(pattern, self._dump)
    #     return result.group(1)

    def _get_id(self) -> str:
        try:
            pattern = r"<id>(.+)</id>"
            result = re.search(pattern, self._dump)
            return result.group(1)
        except:
            return ""

    def _get_description(self) -> str:
        try:
            pattern = r"<text.+>.+((?s:.)+?)(==)"
            result = re.search(pattern, self._dump)
            return result.group(1)
        except:
            return ""

    def toJSON(self, ignore_list = []):
        def default(o):
            d = o.__dict__
            for ignore in ignore_list:
                t = str(type(o).__name__)
                if ignore["className"] == t:
                    for field in ignore["ignore_list"]:
                        d.pop(field)
            return d
        return json.dumps(self, default=default, indent=4)

    def __init__(self, name: str, full_dump: str,):
        self._dump = additional_function.get_one_item(name, full_dump)
        self.name = name
        self.id = self._get_id()
        self.description = self._get_description()
        # print(name)