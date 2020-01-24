import json
import re


class CountriesRegion():

    def add_country(self, country):
        self.countries.append(country)
    def __init__(self, name, descriptions, countries_name):
        self.name = name
        self.descriptions = descriptions
        self.countries_name = countries_name
        self.countries = []

