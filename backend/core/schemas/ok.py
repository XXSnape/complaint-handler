from pydantic import BaseModel


class OkSchema(BaseModel):
    ok: bool = True
