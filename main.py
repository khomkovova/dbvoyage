import region
import country
import additional_function
import json
main_dump = additional_function.get_dump("main.xml")
r = region.Region.init_deep("Funafuti", main_dump, 0)
c = country.Country("United States of America", main_dump)
c.add_all_regions(main_dump)
count = 0
for i in range(len(c.first_layer_regions)-1):
    r0 = c.first_layer_regions[i]
    r0.add_all_regions(main_dump, layer_number = 1)
    for j in range(len(r0.regions)-1):
        r1 = r0.regions[j]
        r1.add_all_regions(main_dump, layer_number = 2)

        for y in range(len(r1.regions) - 1):
            r2 = r1.regions[y]
            r2.add_all_regions(main_dump, layer_number=3)
            r1.regions[y] = r2
            print(count)

        r0.regions[j] = r1


    c.first_layer_regions[i] = r0
pass
# print(c.__dict__)
ignore_list = [
    {"className": "Country", "ignore_list":["_dump", "id", "description"]},
    {"className": "Region", "ignore_list":["_dump", "id", "description"]}
]
report = c.toJSON(ignore_list=ignore_list)
with open("report.txt", "w+") as f:
    f.write(report)



