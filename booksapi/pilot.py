import requests
import pandas as pd


# GET /lists/names.json
get_list_names_url = "https://api.nytimes.com/svc/books/v3/lists/names.json?"

# GET /lists.json
# Get Best Sellers list. If no date is provided returns the latest list.
get_list_url = "https://api.nytimes.com/svc/books/v3/lists.json?"  # list={}(required) & bestsellers-date


def get_list_names(url_prefix, api_key):
    """

    :param url_prefix:
    :param api_key:
    :return:
    """
    try:
        url = url_prefix + "api-key={}".format(api_key)
        response = requests.get(url)
        print("get_list_names response - {}".format(response))
        df = pd.DataFrame(response.json())
        results_df = pd.json_normalize(df["results"])
        return results_df.drop_duplicates(subset="list_name")

    except Exception as exception:
        print("Received Exception in get_list_names function - {}".format(exception))
        raise exception


def get_best_seller_list(url_prefix, api_key, list_name, **kwargs):
    """

    :param url_prefix:
    :param api_key:
    :param list_name:
    :param kwargs:
    :return:
    """
    try:
        if kwargs.get("bestsellers_date"):
            url = url_prefix + "list={}&".format(list_name) + \
                  "bestsellers-date={}&".format(kwargs.get("bestsellers_date")) + "api-key={}".format(api_key)
        else:
            url = url_prefix + "list={}&".format(list_name) + "api-key={}".format(api_key)
        response = requests.get(url)
        print("get_best_seller_list response for {} - {}".format(list_name, response))
        if response:
            if response.json().get("status") == "OK":
                df = pd.DataFrame(response.json())
                results_df = pd.json_normalize(df["results"])
                return True, results_df
            else:
                return None
        else:
            return None

    except Exception as exception:
        print("Received Exception in get_best_seller_list function - {}".format(exception))
        raise exception


def main():
    """

    :return:
    """
    try:
        api_key = "j53zTLkp6zFv7aGI6gzFLQEJl8FyQ9xw"
        list_names = []
        best_sellers = []
        best_seller_ok_list = []
        get_list_names_response = get_list_names(url_prefix=get_list_names_url,
                                                 api_key=api_key).to_dict(orient="records")
        for item in get_list_names_response:
            list_names.append(item.get("list_name"))

        for list_name in list_names:
            get_best_seller_list_response = get_best_seller_list(url_prefix=get_list_url,
                                                                 api_key=api_key, list_name=list_name)
            if get_best_seller_list_response:
                best_seller_ok_list.append(list_name)
                best_sellers.append(get_best_seller_list_response[1])

        print(best_seller_ok_list)
        best_sellers_df = pd.concat(best_sellers, axis=0)


    except Exception as exception:
        print("Received Exception in main function - {}".format(exception))
        raise exception


if __name__ == "__main__":
    main()
