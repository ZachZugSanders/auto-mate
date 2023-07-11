from pydantic import BaseModel


class Authentication(BaseModel):
    target_system: str
    username: str
    password: str


class CommonConfig(BaseModel):
    timeout: int
    max_retries: int
    automation_reports_url: str


class FenrirConfig(BaseModel):
    common: CommonConfig
    auth: Authentication

