from requests import Session, ReadTimeout, Response as ReqResponse
from rest_framework.exceptions import APIException, NotFound
from bs4 import BeautifulSoup


def request_data(session: Session, url: str) -> ReqResponse:
    """
    Request data from url.
    """

    try:
        r = session.get(url, timeout=30)
        return r
    except ReadTimeout:
        raise APIException("Request timeout")
    except Exception:
        raise APIException("Request failed")


def request_post_data(session: Session, url: str, data=None) -> ReqResponse:
    """
    Request post data from url.
    """
    try:
        r = session.post(url, timeout=30, data=data)
        return r
    except ReadTimeout:
        raise APIException("Request timeout")
    except Exception:
        raise APIException("Request failed")


def load_bs4(response: ReqResponse) -> BeautifulSoup:
    """
    Load bs4 from response.
    """
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_captcha_result(soup: BeautifulSoup) -> int:

    captcha_el = soup.select_one(
        "body > table > tr:nth-child(2) > td > table > tr:nth-child(1) > td:nth-child(2) > table > tr:nth-child(2) > td > form > table > tr > td:nth-child(2) > fieldset > table > tr:nth-child(7) > td:nth-child(2)"
    )
    if not captcha_el:
        raise NotFound("captcha element not found")

    values = [int(v) for v in captcha_el.text.split("+")]
    total = sum(values)

    return total


def get_info(soup: BeautifulSoup):
    # select info table
    info_el = soup.select_one(
        "body > table > tr:nth-child(2) > td > table > tr:nth-child(1) > td:nth-child(2) > table > tr:nth-child(2) > td > table > tr:nth-child(1) > td > table"
    )
    if not info_el:
        raise NotFound("result info not found")

    # get table rows
    info_table_rows_el = info_el.find_all("tr")
    info_table_data_list = []
    for info_table_row_el in info_table_rows_el:
        for table_data_el in info_table_row_el:
            table_data = table_data_el.text
            if table_data != "\n":  # ignore empty rows
                info_table_data_list.append(table_data.strip())

    # sanitize data into key, value
    info_table_data_sanitized = []
    for a, b in zip(info_table_data_list[::2], info_table_data_list[1::2]):
        info_table_data_sanitized.append({"key": a, "value": b})

    # return sanitized data
    return info_table_data_sanitized


def get_grades(soup: BeautifulSoup):
    # select grades table
    grades_el = soup.select_one(
        "body > table > tr:nth-child(2) > td > table > tr:nth-child(1) > td:nth-child(2) > table > tr:nth-child(2) > td > table > tr:nth-child(3) > td > table"
    )
    if not grades_el:
        raise NotFound("result grades not found")

    # get table rows
    grades_table_rows_el = grades_el.find_all("tr")
    grades_table_data_list = []
    for grades_table_row in grades_table_rows_el:
        if not (
            grades_table_row.has_attr("class")
            and grades_table_row["class"][0] == "black12bold"
        ):
            for table_data_el in grades_table_row:
                table_data = table_data_el.text
                if table_data != "\n":  # ignore empty rows
                    grades_table_data_list.append(table_data.strip())

    # sanitize data into code, subject and grade
    grades_table_data_list_sanitized = []
    for a, b, c in zip(
        grades_table_data_list[::3],
        grades_table_data_list[1::3],
        grades_table_data_list[2::3],
    ):
        grades_table_data_list_sanitized.append({"code": a, "subject": b, "grade": c})

    # return sanitized data
    return grades_table_data_list_sanitized


# def get_element_options(element_selector: str, soup: BeautifulSoup) -> list:
#     """
#     Get options of a select element.
#     """
#     # examination
#     element = soup.select_one(element_selector)
#     if not element:
#         raise NotFound(f"{element_selector} element not found")
#     option_el_list = element.find_all("option")

#     option_list = []
#     for option_el in option_el_list:
#         value = option_el.attrs["value"]
#         text = option_el.text
#         info = {"value": value, "text": text}
#         option_list.append(info)
#     return option_list
