"""Enoten ukaz za prenos OSM podatkov in posodobitev podatkovne baze."""

from Data.download_osm import main as prenesi
from Data.import_json import main as uvozi


def main():
    prenesi()
    uvozi()


if __name__ == "__main__":
    main()
