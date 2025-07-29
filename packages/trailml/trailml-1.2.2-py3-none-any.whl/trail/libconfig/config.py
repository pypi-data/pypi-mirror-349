import os
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENDPOINT_URL: str = ""
    PRESIGNED_ENDPOINT: str = "/generate_presigned_bucket_url"
    GQL_ENDPOINT: str = "/graphql"

    PRIMARY_USER_CONFIG_PATH: str = "trail_config.yml"
    TRAIL_CONFIG_PATH: str = os.getcwd()

    TRAIL_SIGN_UP_URL: str = "https://www.trail-ml.com/sign-up"

    def presigned_endpoint_url(self, user_specific_endpoint: str = "") -> str:
        if user_specific_endpoint:
            return user_specific_endpoint + self.PRESIGNED_ENDPOINT
        return self.ENDPOINT_URL + self.PRESIGNED_ENDPOINT

    def gql_endpoint_url(self, user_specific_endpoint: str = "") -> str:
        if user_specific_endpoint:
            return user_specific_endpoint + self.GQL_ENDPOINT
        return self.ENDPOINT_URL + self.GQL_ENDPOINT


class ProductionConfig(Config):
    ENDPOINT_URL: str = "https://gql.trail-ml.com"


class DevelopmentConfig(Config):
    ENDPOINT_URL: str = "http://127.0.0.1:5002"
