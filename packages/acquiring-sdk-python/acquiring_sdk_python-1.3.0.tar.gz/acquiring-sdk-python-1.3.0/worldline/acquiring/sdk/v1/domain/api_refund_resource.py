# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from datetime import datetime
from typing import List, Optional

from .amount_data import AmountData
from .api_references_for_responses import ApiReferencesForResponses
from .card_payment_data_for_resource import CardPaymentDataForResource
from .sub_operation_for_refund import SubOperationForRefund

from worldline.acquiring.sdk.domain.data_object import DataObject


class ApiRefundResource(DataObject):

    __card_payment_data: Optional[CardPaymentDataForResource] = None
    __initial_authorization_code: Optional[str] = None
    __operations: Optional[List[SubOperationForRefund]] = None
    __referenced_payment_id: Optional[str] = None
    __references: Optional[ApiReferencesForResponses] = None
    __refund_id: Optional[str] = None
    __status: Optional[str] = None
    __status_timestamp: Optional[datetime] = None
    __total_authorized_amount: Optional[AmountData] = None

    @property
    def card_payment_data(self) -> Optional[CardPaymentDataForResource]:
        """
        Type: :class:`worldline.acquiring.sdk.v1.domain.card_payment_data_for_resource.CardPaymentDataForResource`
        """
        return self.__card_payment_data

    @card_payment_data.setter
    def card_payment_data(self, value: Optional[CardPaymentDataForResource]) -> None:
        self.__card_payment_data = value

    @property
    def initial_authorization_code(self) -> Optional[str]:
        """
        | Authorization approval code

        Type: str
        """
        return self.__initial_authorization_code

    @initial_authorization_code.setter
    def initial_authorization_code(self, value: Optional[str]) -> None:
        self.__initial_authorization_code = value

    @property
    def operations(self) -> Optional[List[SubOperationForRefund]]:
        """
        Type: list[:class:`worldline.acquiring.sdk.v1.domain.sub_operation_for_refund.SubOperationForRefund`]
        """
        return self.__operations

    @operations.setter
    def operations(self, value: Optional[List[SubOperationForRefund]]) -> None:
        self.__operations = value

    @property
    def referenced_payment_id(self) -> Optional[str]:
        """
        | The identifier of the payment referenced by this refund.

        Type: str
        """
        return self.__referenced_payment_id

    @referenced_payment_id.setter
    def referenced_payment_id(self, value: Optional[str]) -> None:
        self.__referenced_payment_id = value

    @property
    def references(self) -> Optional[ApiReferencesForResponses]:
        """
        | A set of references returned in responses

        Type: :class:`worldline.acquiring.sdk.v1.domain.api_references_for_responses.ApiReferencesForResponses`
        """
        return self.__references

    @references.setter
    def references(self, value: Optional[ApiReferencesForResponses]) -> None:
        self.__references = value

    @property
    def refund_id(self) -> Optional[str]:
        """
        | the ID of the refund

        Type: str
        """
        return self.__refund_id

    @refund_id.setter
    def refund_id(self, value: Optional[str]) -> None:
        self.__refund_id = value

    @property
    def status(self) -> Optional[str]:
        """
        | The status of the payment, refund or credit transfer
        | Possible values are:
        
        * AUTHORIZED
        * NOT_AUTHORIZED
        * PENDING
        * PENDING_CAPTURE
        * CONFIRMED
        * REVERSED
        * CANCELLED

        Type: str
        """
        return self.__status

    @status.setter
    def status(self, value: Optional[str]) -> None:
        self.__status = value

    @property
    def status_timestamp(self) -> Optional[datetime]:
        """
        | Timestamp of the status in format yyyy-MM-ddTHH:mm:ssZ

        Type: datetime
        """
        return self.__status_timestamp

    @status_timestamp.setter
    def status_timestamp(self, value: Optional[datetime]) -> None:
        self.__status_timestamp = value

    @property
    def total_authorized_amount(self) -> Optional[AmountData]:
        """
        | Amount for the operation.

        Type: :class:`worldline.acquiring.sdk.v1.domain.amount_data.AmountData`
        """
        return self.__total_authorized_amount

    @total_authorized_amount.setter
    def total_authorized_amount(self, value: Optional[AmountData]) -> None:
        self.__total_authorized_amount = value

    def to_dictionary(self) -> dict:
        dictionary = super(ApiRefundResource, self).to_dictionary()
        if self.card_payment_data is not None:
            dictionary['cardPaymentData'] = self.card_payment_data.to_dictionary()
        if self.initial_authorization_code is not None:
            dictionary['initialAuthorizationCode'] = self.initial_authorization_code
        if self.operations is not None:
            dictionary['operations'] = []
            for element in self.operations:
                if element is not None:
                    dictionary['operations'].append(element.to_dictionary())
        if self.referenced_payment_id is not None:
            dictionary['referencedPaymentId'] = self.referenced_payment_id
        if self.references is not None:
            dictionary['references'] = self.references.to_dictionary()
        if self.refund_id is not None:
            dictionary['refundId'] = self.refund_id
        if self.status is not None:
            dictionary['status'] = self.status
        if self.status_timestamp is not None:
            dictionary['statusTimestamp'] = DataObject.format_datetime(self.status_timestamp)
        if self.total_authorized_amount is not None:
            dictionary['totalAuthorizedAmount'] = self.total_authorized_amount.to_dictionary()
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'ApiRefundResource':
        super(ApiRefundResource, self).from_dictionary(dictionary)
        if 'cardPaymentData' in dictionary:
            if not isinstance(dictionary['cardPaymentData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['cardPaymentData']))
            value = CardPaymentDataForResource()
            self.card_payment_data = value.from_dictionary(dictionary['cardPaymentData'])
        if 'initialAuthorizationCode' in dictionary:
            self.initial_authorization_code = dictionary['initialAuthorizationCode']
        if 'operations' in dictionary:
            if not isinstance(dictionary['operations'], list):
                raise TypeError('value \'{}\' is not a list'.format(dictionary['operations']))
            self.operations = []
            for element in dictionary['operations']:
                value = SubOperationForRefund()
                self.operations.append(value.from_dictionary(element))
        if 'referencedPaymentId' in dictionary:
            self.referenced_payment_id = dictionary['referencedPaymentId']
        if 'references' in dictionary:
            if not isinstance(dictionary['references'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['references']))
            value = ApiReferencesForResponses()
            self.references = value.from_dictionary(dictionary['references'])
        if 'refundId' in dictionary:
            self.refund_id = dictionary['refundId']
        if 'status' in dictionary:
            self.status = dictionary['status']
        if 'statusTimestamp' in dictionary:
            self.status_timestamp = DataObject.parse_datetime(dictionary['statusTimestamp'])
        if 'totalAuthorizedAmount' in dictionary:
            if not isinstance(dictionary['totalAuthorizedAmount'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['totalAuthorizedAmount']))
            value = AmountData()
            self.total_authorized_amount = value.from_dictionary(dictionary['totalAuthorizedAmount'])
        return self
