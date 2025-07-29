from brynq_sdk_brynq import BrynQ
import requests
from typing import List, Union, Literal, Optional
from .costcentres import Costcentres
from .deductions import Deductions
from .departments import Departments
from .employees import Employees
from .payments import Payments


# Set the base class for Factorial. This class will be used to set the credentials and those will be used in all other classes.
class Sage(BrynQ):
    def __init__(self, system_type: Optional[Literal['source', 'target']] = None, debug: bool = False):
        """"
        For the documentation of Sage, see the PaySDO.chm file.
        Also check the Sage agent docs at: https://sage.app.brynq.com/swagger/index.html (running on QAP staging)
        """
        super().__init__()
        headers, base_url = self._get_credentials(system_type)
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.employees = Employees(headers=headers, base_url=base_url)
        self.costcentres = Costcentres(headers=headers, base_url=base_url)
        self.deductions = Deductions(headers=headers, base_url=base_url)
        self.payments = Payments(headers=headers, base_url=base_url)
        self.departments = Departments(headers=headers, base_url=base_url)
        self.employees = Employees(headers=headers, base_url=base_url)
        self.debug = debug

    def _get_credentials(self, system_type):
        """
        Sets the credentials for the SuccessFactors API.
        :param label (str): The label for the system credentials.
        :returns: headers (dict): The headers for the API request, including the access token.
        """
        credentials = self.interfaces.credentials.get(system="sage", system_type=system_type)
        credentials = credentials.get('data')
        url = credentials['url']
        headers = {
            'Authorization': f"Bearer {credentials['access_token']}",
            "domain": f"{credentials['domain']}",
            'Content-Type': 'application/json'
        }

        return headers, url

