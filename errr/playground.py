import inspect
import json
import random
import sys
from types import TracebackType
from typing import List, Type

import httpx

from errr.models import Error, Frame, PythonEntity, Report
from errr.utils import get_object_type_str


def report_frame(e_type: Type[BaseException], e_value: BaseException, e_traceback: TracebackType):

    stack: List[Frame] = []

    counter = 0

    current_frame = e_traceback.tb_frame
    current_tb = e_traceback
    tb_lineno = 1
    while current_tb and counter < 10:

        f_locals: List[PythonEntity] = []

        for name, local in current_tb.tb_frame.f_locals.items():
            f_locals.append(PythonEntity(name=name, value=str(local), type=get_object_type_str(local)))

        stack.append(
            Frame(
                lineno=current_frame.f_code.co_firstlineno,
                source="-" or inspect.getsource(current_frame),
                filename=current_frame.f_code.co_filename,
                locals=f_locals,
            )
        )

        counter += 1
        current_tb = current_tb.tb_next

    error = Error(type=(str(e_type)), value=str(e_value), lineno=current_tb.tb_lineno)
    report = Report(stack=stack, error=error)

    print(report.json())


async def two():

    x = "ok"
    y = "yeet"
    z = f"{x} {y}"

    random.random()

    async with httpx.AsyncClient() as client:
        res = await client.get("https://api.braiseapp.com")

        s = res.status_code

    y = res.json()

    1 / 0


async def one():

    a = 1
    b = 2
    c = a + b

    await two()


if __name__ == "__main__":
    import asyncio

    sys.excepthook = report_frame

    asyncio.run(one())
