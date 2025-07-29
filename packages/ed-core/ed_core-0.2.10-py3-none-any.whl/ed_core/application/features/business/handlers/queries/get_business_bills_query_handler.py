from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.business.requests.queries import \
    GetBusinessBillsQuery
from ed_core.application.features.common.dtos import BillDto


@request_handler(GetBusinessBillsQuery, BaseResponse[list[BillDto]])
class GetBusinessBillsQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetBusinessBillsQuery
    ) -> BaseResponse[list[BillDto]]:
        if business := self._uow.business_repository.get(id=request.business_id):
            bill_ids = business["bills"]

            if not bill_ids:
                raise ApplicationException(
                    Exceptions.NotFoundException,
                    "Business bills could not fetched.",
                    [f"Bills for business with id {request.business_id} not found."],
                )

            bill_id_dtos = []
            for bill_id in bill_ids:
                bill = self._uow.bill_repository.get(id=bill_id)
                if not bill:
                    raise ApplicationException(
                        Exceptions.NotFoundException,
                        "Business bills could not fetched.",
                        [f"Bill with id {bill_id} not found."],
                    )
                bill_id_dtos.append(BillDto.from_bill(bill))

        raise ApplicationException(
            Exceptions.NotFoundException,
            "Business bills could not fetched.",
            [f"Business with id {request.business_id} not found."],
        )
