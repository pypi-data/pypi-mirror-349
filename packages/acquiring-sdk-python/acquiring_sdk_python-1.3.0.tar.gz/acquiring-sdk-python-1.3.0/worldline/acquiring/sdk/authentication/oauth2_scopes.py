# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Callable, Set


class OAuth2Scopes(object):

    __scopes_by_operation = {
        "v1": {
            "processPayment": ["processing_payment"],
            "getPaymentStatus": ["processing_payment"],
            "simpleCaptureOfPayment": ["processing_payment"],
            "reverseAuthorization": ["processing_payment"],
            "incrementPayment": ["processing_payment"],
            "createRefund": ["processing_refund"],
            "processStandaloneRefund": ["processing_refund"],
            "getRefund": ["processing_refund"],
            "captureRefund": ["processing_refund"],
            "reverseRefundAuthorization": ["processing_refund"],
            "processAccountVerification": ["processing_accountverification"],
            "processBalanceInquiry": ["processing_balanceinquiry"],
            "technicalReversal": ["processing_operation_reverse"],
            "requestDccRate": ["processing_dcc_rate"],
            "ping": ["services_ping"]
        }
    }

    __all_scopes = None

    @staticmethod
    def all() -> Set[str]:
        """
        Returns all available scopes.
        """
        if not OAuth2Scopes.__all_scopes:
            result = []
            for operations in OAuth2Scopes.__scopes_by_operation.values():
                for scopes in operations.values():
                    result += scopes
            OAuth2Scopes.__all_scopes = set(result)

        return set(OAuth2Scopes.__all_scopes)

    @staticmethod
    def for_api_version(api_version: str) -> Set[str]:
        """
        Returns all scopes needed for all operations of the given API version.
        """
        operations = OAuth2Scopes.__scopes_by_operation.get(api_version, {})
        result = []
        for scopes in operations.values():
            result += scopes
        return set(result)

    @staticmethod
    def for_operation(api_version: str, operation_id: str) -> Set[str]:
        """
        Returns all scopes needed for the given operation of the given API version.
        """
        operations = OAuth2Scopes.__scopes_by_operation.get(api_version, {})
        return set(operations.get(operation_id, []))

    @staticmethod
    def for_operations(api_version: str, *operation_ids: str) -> Set[str]:
        """
        Returns all scopes needed for the given operations of the given API version.
        """
        operations = OAuth2Scopes.__scopes_by_operation.get(api_version, {})
        result = []
        for operation_id in operation_ids:
            result += operations.get(operation_id, [])
        return set(result)

    @staticmethod
    def for_filtered_operations(operation_filter: Callable[[str, str], bool]) -> Set[str]:
        """
        Returns all scopes needed for the operations that pass the given filter.
        The first argument to the filter is the API version, the second is the operation id.
        """
        result = []
        for api_version, operations in OAuth2Scopes.__scopes_by_operation.items():
            for operation_id, scopes in operations.items():
                if operation_filter(api_version, operation_id):
                    result += scopes
        return set(result)
