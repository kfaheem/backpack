import requests
import pandas as pd
import os


# GET /lists/names.json
# Get Best Sellers list names.
get_list_names_url = "https://api.nytimes.com/svc/books/v3/lists/names.json?"

# GET /lists.json
# Get Best Sellers list. If no date is provided returns the latest list.
get_list_url = "https://api.nytimes.com/svc/books/v3/lists.json?"
# list={}(required) & bestsellers-date & published-date & offset


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
        if response:
            if response.json().get("status") == "OK":
                df = pd.DataFrame(response.json())
                results_df = pd.json_normalize(df["results"])
                return True, results_df.drop_duplicates(subset="list_name")
        else:
            return False

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
                results_df["Title"] = results_df.apply(lambda row: row["book_details"][0].get("title"), axis=1)
                results_df["Description"] = results_df.apply(lambda row: row["book_details"][0].get("description"),
                                                             axis=1)
                results_df["Author"] = results_df.apply(lambda row: row["book_details"][0].get("author"), axis=1)
                return True, results_df
            else:
                return None
        else:
            return None

    except Exception as exception:
        print("Received Exception in get_best_seller_list function - {}".format(exception))
        raise exception


def create_csv(best_sellers_df, **kwargs):
    """

    :param best_sellers_df:
    :param kwargs:
    :return:
    """
    try:
        if kwargs.get("csv_path"):
            csv_path = kwargs.get("csv_path")
        else:
            csv_path = "{}/nyt_best_sellers.csv".format(os.getcwd())
        best_sellers_df.to_csv(csv_path, header=True)
        return True

    except Exception as exception:
        print("Received Exception in create_csv function - {}".format(exception))
        raise exception


def main():
    """

    :return:
    """
    try:
        api_key = os.environ.get("api_key")
        if api_key:
            list_names = []
            best_sellers = []
            best_seller_ok_list = []
            get_list_names_response = get_list_names(url_prefix=get_list_names_url,
                                                     api_key=api_key)
            if get_list_names_response:
                for item in get_list_names_response[1].to_dict(orient="records"):
                    list_names.append(item.get("list_name"))

                for list_name in list_names:
                    get_best_seller_list_response = get_best_seller_list(url_prefix=get_list_url,
                                                                         api_key=api_key, list_name=list_name)
                    if get_best_seller_list_response:
                        best_seller_ok_list.append(list_name)
                        best_sellers.append(get_best_seller_list_response[1])

                best_sellers_df = pd.concat(best_sellers, axis=0)
                create_csv(best_sellers_df=best_sellers_df
            else:
                print("No list names received")

        else:
            print("Please pass the api-key as an env var")

    except Exception as exception:
        print("Received Exception in main function - {}".format(exception))
        raise exception


if __name__ == "__main__":
    main()
