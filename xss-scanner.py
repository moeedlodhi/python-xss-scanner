import sys
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


XSS_SCRIPT = "<Script>alert('hi')</scripT>"

class MissingUrlException(Exception):
    pass


class BaseXSSScanner:
    def __init__(self, url):
        if not url:
            raise MissingUrlException('Url is required to run scanner.')
        
        self.url = url
        self.js_script = XSS_SCRIPT
        
    def _extract_forms(self, url):
        """
        Extract all forms from url.
        """
        soup = bs(requests.get(url).content, "html.parser")
        return soup.find_all("form")


    def get_form_details(self, form):
        """
        Extract details from form like method, url, and inputs.
        """
        raise NotImplementedError('Please implement get_form_details as per your needs.')


    def _submit_form(self, form_details, url, value):
        """
        Submits a form using form_details.
        """
        target_url = urljoin(url, form_details["action"])
        inputs = form_details["inputs"]
        data = {}
        for input in inputs:
            if input["type"] == "text" or input["type"] == "search":
                input["value"] = value

            input_name = input.get("name")
            input_value = input.get("value")
            if input_name and input_value:
                data[input_name] = input_value

        if form_details["method"] == "post":
            return requests.post(target_url, data=data)
        else:
            return requests.get(target_url, params=data)


    def scan(self, url):
        """
        Given a url, it prints all XSS vulnerable forms.
        """
        forms = self._extract_forms(url)
        print(f"[+] Detected {len(forms)} forms on {url}.")

        for form in forms:
            form_details = self.get_form_details(form)
            content = self._submit_form(form_details, url, self.js_script).content.decode()
            if self.js_script in content:
                print(f"[+] XSS Detected on {url}")
                print(f"[*] Form details:")
                pprint(form_details)


class XSSGameScanner(BaseXSSScanner):

    def get_form_details(self, form):
        details = {}
        action = form.attrs.get("action").lower()
        method = form.attrs.get("method", "get").lower()
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            inputs.append({"type": input_type, "name": input_name})

        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details


if __name__ == "__main__":    
    url = sys.argv[1]
    scanner = XSSGameScanner(url)
    scanner.scan(url)
