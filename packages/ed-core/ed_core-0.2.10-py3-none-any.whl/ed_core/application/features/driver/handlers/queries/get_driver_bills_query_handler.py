from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import BillDto
from ed_core.application.features.driver.requests.queries import \
    GetDriverBillsQuery


@request_handler(GetDriverBillsQuery, BaseResponse[list[BillDto]])
class GetDriverBillsQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: GetDriverBillsQuery) -> BaseResponse[list[BillDto]]:
        if driver := self._uow.driver_repository.get(id=request.driver_id):
            bill_ids = driver["bill_ids"]

            if not bill_ids:
                raise ApplicationException(
                    Exceptions.NotFoundException,
                    "Driver bills could not fetched.",
                    [f"Bills for driver with id {request.driver_id} not found."],
                )

            bill_id_dtos = []
            for bill_id in bill_ids:
                bill = self._uow.bill_repository.get(id=bill_id)
                if not bill:
                    raise ApplicationException(
                        Exceptions.NotFoundException,
                        "Driver bills could not fetched.",
                        [f"Bill with id {bill_id} not found."],
                    )
                bill_id_dtos.append(BillDto.from_bill(bill))

        raise ApplicationException(
            Exceptions.NotFoundException,
            "Driver bills could not fetched.",
            [f"Driver with id {request.driver_id} not found."],
        )
