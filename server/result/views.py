from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError, NotFound
from requests import Session

from .serializers import ResultSerializer

from .services import (
    get_grades,
    get_info,
    request_data,
    load_bs4,
    get_captcha_result,
    request_post_data,
)


class ResultAPIView(GenericAPIView):
    serializer_class = ResultSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        # serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        with Session() as s:
            # request -> to get captcha
            form_response = request_data(
                session=s, url="http://www.educationboardresults.gov.bd/"
            )

            #
            form_soup = load_bs4(form_response)

            # captcha
            captcha = get_captcha_result(soup=form_soup)

            # send form data request
            form_data = {
                "sr": "2",
                "et": "3",
                "exam": data["exam"],
                "year": data["year"],
                "board": data["board"],
                "roll": data["roll"],
                "reg": data["reg"],
                "value_s": captcha,
                "button2": "Submit",
            }

            result_response = request_post_data(
                session=s,
                url="http://www.educationboardresults.gov.bd/result.php",
                data=form_data,
            )
            if "?err" in result_response.text:
                raise ValidationError({"message": "Invalid data"})

            # result
            result_soup = load_bs4(result_response)

            # get info
            info = get_info(soup=result_soup)
            # get grades
            grades = get_grades(soup=result_soup)

            return Response({"info": info, "grades": grades})


# class InfoAPIView(APIView):
#     def get(self, request: Request, *args, **kwargs) -> Response:
#         with Session() as s:
#             response = request_data(
#                 session=s, url="http://www.educationboardresults.gov.bd/"
#             )

#             #
#             soup = load_bs4(response)

#             #
#             exam_options = get_element_options(element_selector="#exam", soup=soup)
#             year_options = get_element_options(element_selector="#year", soup=soup)
#             board_options = get_element_options(element_selector="#board", soup=soup)

#             #
#             return Response(
#                 {
#                     "exam_options": exam_options,
#                     "year_options": year_options,
#                     "board_options": board_options,
#                 }
#             )
