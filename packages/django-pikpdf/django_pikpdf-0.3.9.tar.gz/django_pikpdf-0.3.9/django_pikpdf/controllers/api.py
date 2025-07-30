import base64
from dataclasses import dataclass
import json
from typing import Optional
import requests
from django.conf import settings

FORMAT_CHOICES = {
    "A4": "A4",
    "A5": "A5",
    "A6": "A6",
    "Letter": "Letter",
}

@dataclass
class PdfApiParams:
    '''
        Class for api params
    '''
    display_header_footer:bool = False
    format:str = FORMAT_CHOICES["A4"]
    landscape:bool = False
    print_background:bool = False
    prefer_css_page_size:bool = True
    scale:float = 1.0
    margin_top:int = 0
    margin_bottom:int = 0
    margin_left:int = 0
    margin_right:int = 0
    auth_token_name:Optional[str] = None
    auth_token_value:Optional[str] = None

    def to_json(self) -> str:
        '''
            Returns json string of the class
        '''
        return json.dumps(self.__dict__)


def get_api_token() -> str:
    '''
        Returns pikutis api token
    '''
    return settings.PIKUTIS_API_KEY

def call_pdf_api(file_string:str, api_params:Optional[PdfApiParams]) -> dict:
    '''
        Calls pikutis api and returns response
    '''
    api_url:str = "https://www.pikutis.lt/api/generate-pdf/"
    if settings.DEBUG:
        api_url = "http://localhost:8000/api/generate-pdf/"
    pdf_request:requests.Request = requests.Request('POST', url=api_url)
    pdf_request.headers = {"Token": get_api_token()}
    pdf_request.data = file_string.encode('utf-8')
    if api_params:
        pdf_request.params = api_params.to_json()

    pdf_response:requests.Response = requests.Session().send(pdf_request.prepare())
    return json.loads(pdf_response.content)

def get_pdf_file(pdf_response:dict) -> bytes:
    '''
        Returns pdf file bytes
    '''
    return base64.b64decode(pdf_response['file_bytes_base_64'])