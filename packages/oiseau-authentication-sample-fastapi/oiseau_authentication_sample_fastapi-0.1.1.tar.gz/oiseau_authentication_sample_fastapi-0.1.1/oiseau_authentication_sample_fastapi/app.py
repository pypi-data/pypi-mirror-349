"""
Run de l'application demo
Il faut se connecter directement sur l'app en utilisant le client localhost-frontend
"""

from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI

from oiseau_authentification.configuration.oidc.fastapi_oidc_configuration import \
    FastAPIOIDCConfiguration
from oiseau_authentification.decorators.authenticate_token import \
    authentication_token_oidc_oiseau
from oiseau_authentification.model.parsed_token import ParsedToken
from oiseau_authentification.routers.user_router import \
    create_user_router_from_configuration

oidc_configuration = FastAPIOIDCConfiguration(
    "localhost-frontend",
    None,
    "https://auth.insee.test/auth/realms/agents-insee-interne/.well-known/openid-configuration",
    "account",
)


app = FastAPI(root = "/oiseau-authentication/", openapi_url="/oiseau-authentication/openapi.json",swagger_ui_init_oauth=oidc_configuration.get_swagger_init_oauth())
app.include_router(
    create_user_router_from_configuration(configuration=oidc_configuration)
)


app.include_router(
    create_user_router_from_configuration(configuration=oidc_configuration)
)


@app.get(
    "/authenticated", dependencies=[Depends(oidc_configuration.authorization_code())]
)
@authentication_token_oidc_oiseau
async def authenticated(
    application: str,
    token: str | ParsedToken = Depends(oidc_configuration.authorization_code()),
):
    return {"message": f"Hello {token.preferred_username}"}


@app.get(
    "/authenticated/{authenticate-group}",
    dependencies=[Depends(oidc_configuration.authorization_code())],
)
@authentication_token_oidc_oiseau
async def authenticated(
    application: str,
    token: str | ParsedToken = Depends(oidc_configuration.authorization_code()),
    authenticate_group: Optional[str] = None,
):
    return {
        "message": f"Etant dans le groupe {authenticate_group}, vous, {token.preferred_username} avez accès a cette ressource"
    }

@authentication_token_oidc_oiseau
async def authenticated_(
    application: str,
    token: str | ParsedToken = Depends(oidc_configuration.authorization_code()),
    authenticate_group: Optional[str] = None,
):
    return {
        "message": f"Etant dans le groupe {authenticate_group}, vous, {token.preferred_username} avez accès a cette ressource"
    }



@app.get("/unauthenticated")
async def unauthenticated():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000)
