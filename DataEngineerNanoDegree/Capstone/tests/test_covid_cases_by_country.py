import pytest
from DataEngineerNanoDegree.Capstone.covid_cases_by_country import get_countries, get_unique_countries


def test_get_countries():
    """
    The test validates if the Covid19API returns Country Name United States
    :return:
    """
    countries_api_endpoint = "https://api.covid19api.com/countries"
    countries = get_countries(api_endpoint=countries_api_endpoint)

    expected_output = "United States"
    actual_result = ""
    for item in countries:
        if item.get("Country Name") == "United States":
            actual_result = "United States"

    assert expected_output == actual_result


def test_get_unique_countries():
    """
    The test validates if the correct object structure is maintained after the get_unique_countries function is
    executed.
    :return:
    """
    # expected_object_structure = {"Country Name": "United States", Slug": "united - states", "ISO2":"US"}

    countries = [{"Country Name": "United States", "Slug": "united - states", "ISO2":"US"},
                 {"Country Name": "China", "Slug": "united - china", "ISO2":"CN"},
                 {"Country Name": "India", "Slug": "india", "ISO2":"IN"}]

    unique_countries = get_unique_countries(countries)

    expected_country_key = "Country Name"

    actual_output = unique_countries[0]

    actual_output_country_key = ""

    for key, value in actual_output:
        if key == "Country Name":
            actual_output_country_key = "Country Name"
            break

    assert expected_country_key == actual_output_country_key