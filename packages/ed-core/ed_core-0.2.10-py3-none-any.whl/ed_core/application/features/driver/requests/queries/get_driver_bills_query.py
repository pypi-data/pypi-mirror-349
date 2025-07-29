from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.types import Request

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import BillDto


@request(BaseResponse[list[BillDto]])
@dataclass
class GetDriverBillsQuery(Request):
    driver_id: UUID
