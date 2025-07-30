from functools import wraps

from jose import jwt
from jwt import PyJWKClient
from jwt.exceptions import InvalidTokenError
import base64
import json
KEYCLOAK_URL = "https://backbase.datumhq.com/auth"
REALM = "shared_auth_dev"
ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"
AUDIENCE = "account"  # as per your token
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
import urllib.request

shared_secret = "tZAvHdqd7daVb8Wlpu6aaf62tm7ltllO".strip()
def get_jwt_header(token: str) -> dict:
    header_b64 = token.split('.')[0]
    header_b64 += '=' * (-len(header_b64) % 4)  # pad base64 if needed
    decoded = base64.urlsafe_b64decode(header_b64)
    return json.loads(decoded)
#
# try:
#     header = get_jwt_header(token)
#     alg = header.get("alg")
#     kid = header.get("kid")
#
#     if alg == "HS512":
#         payload = jwt.decode(
#             token,
#             shared_secret,
#             algorithms=["HS512"],
#             options={"verify_aud": False}
#         )
#         print(payload)
#     elif alg == "RS256" or "ES256":
#         jwk_client = PyJWKClient(JWKS_URL)
#         signing_key = jwk_client.get_signing_key_from_jwt(token)
#
#         payload = jwt.decode(
#             token,
#             signing_key.key,
#             algorithms=None,  # Accept all supported algorithms
#             issuer=ISSUER,
#             audience=AUDIENCE  # Optional: include if you expect it
#         )
#
#     print(" Token is valid. Payload:")
# except InvalidTokenError as e:
#     print(f" Invalid token: {e}")
def extract_roles(payload):
    try:
        return payload['realm_access']['roles']
    except KeyError:
        return []


def get_public_key(token):
    try:
        jwk_client = PyJWKClient(JWKS_URL)
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        return signing_key.key
    except Exception as e:
        raise Exception(f"Unable to fetch Keycloak signing key: {e}")

class CustomPyJWKClient(PyJWKClient):
    def fetch_data(self):
        req = urllib.request.Request(
            self.uri,
            headers={"User-Agent": "Mozilla/5.0"}  # Prevent 403 from WAFs
        )
        with urllib.request.urlopen(req) as response:
            raw = response.read()
            try:
                return json.loads(raw)  # ✅ parse JSON here
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Failed to decode JSON from JWKS endpoint. Raw response: {raw[:300]}"
                ) from e

def keycloak_token_required(issuer, audience):

    def decorator(func):
        @wraps(func)
        def wrapper(event, context, *args, **kwargs):
            try:
                auth_header = event["headers"].get("Authorization", "")
                if not auth_header.startswith("Bearer "):
                    raise Exception("Missing or invalid Authorization header")

                token = auth_header.split(" ")[1]
                header = get_jwt_header(token)
                alg = header.get("alg")
                if alg == "HS512":
                    decoded_token = jwt.decode(
                        token,
                        shared_secret,
                        algorithms=[alg],
                        options={"verify_aud": False}
                    )
                elif alg == "RS256" or "ES256":
                    jwk_client = CustomPyJWKClient(JWKS_URL)

                    # jwk_client = PyJWKClient(JWKS_URL)
                    signing_key = jwk_client.get_signing_key_from_jwt(token)

                    decoded_token = jwt.decode(
                        token,
                        signing_key.key,
                        algorithms=[alg],
                        audience=AUDIENCE,
                        issuer=ISSUER,
                        options={"verify_exp": True}
                    )

                event["decoded_token"] = decoded_token  # Pass it along

                queryStringParameters = event['queryStringParameters']
                pathParameters = event['pathParameters']
                stageVariables = event['stageVariables']

                # Parse the input for the parameter values
                tmp = event['methodArn'].split(':')
                apiGatewayArnTmp = tmp[5].split('/')
                awsAccountId = tmp[4]
                region = tmp[3]
                restApiId = apiGatewayArnTmp[0]
                stage = apiGatewayArnTmp[1]
                method = apiGatewayArnTmp[2]
                resource = '/'

                if (apiGatewayArnTmp[3]):
                    resource += apiGatewayArnTmp[3]

                    # Perform authorization to return the Allow policy for correct parameters
                    # and the 'Unauthorized' error, otherwise.
                headers = event['headers']

                if (headers['HeaderAuth1'] == "headerValue1" and queryStringParameters[
                    'QueryString1'] == "queryValue1" and stageVariables['StageVar1'] == "stageValue1"):
                    response = generateAllow('me', event['methodArn'])
                    print('authorized')
                    response
                else:
                    print('unauthorized')
                    response = generateDeny('me', event['methodArn'])

                return response

            except Exception as e:
                return {
                    "statusCode": 401,
                    "body": json.dumps({"message": "Unauthorized", "error": str(e)})
                }

        return wrapper
    return decorator

def generatePolicy(principalId, effect, resource, decoded_token):
    authResponse = {}
    authResponse['principalId'] = principalId
    if (effect and resource):
        policyDocument = {}
        policyDocument['Version'] = '2012-10-17'
        policyDocument['Statement'] = []
        statementOne = {}
        statementOne['Action'] = 'execute-api:Invoke'
        statementOne['Effect'] = effect
        statementOne['Resource'] = resource
        policyDocument['Statement'] = [statementOne]
        authResponse['policyDocument'] = policyDocument

    authResponse['context'] = decoded_token

    return authResponse


def generateAllow(principalId, resource):
    return generatePolicy(principalId, 'Allow', resource)


def generateDeny(principalId, resource):
    return generatePolicy(principalId, 'Deny', resource)

event = {
    "headers": {
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJWZXNOcktyZXpxNl93dVNFRXY0TllTX3hDYkgwaV83Y25XeWQxWWVHUDFVIn0.eyJleHAiOjE3NDc5NDk2NjMsImlhdCI6MTc0NzkzMTY2MywiYXV0aF90aW1lIjoxNzQ3OTMxNjQ2LCJqdGkiOiJkMDU3MDhlOS04NjBhLTRlNmEtOTE2MC03MWU0MTkyNjg5NjQiLCJpc3MiOiJodHRwczovL2JhY2tiYXNlLmRhdHVtaHEuY29tL2F1dGgvcmVhbG1zL3NoYXJlZF9hdXRoX2RldiIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiI1NTk1YTRlZC1mYzUyLTQ0YmYtYjA3NC1mYTYzZDc5YmZjZTAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJob2FuZyIsInNlc3Npb25fc3RhdGUiOiJlZjg0ZDc4Ny1jNmVkLTRlOGQtYTk1NS0xNjdhZDVjMTVkZDkiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXNoYXJlZF9hdXRoX2RldiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiJlZjg0ZDc4Ny1jNmVkLTRlOGQtYTk1NS0xNjdhZDVjMTVkZDkiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6ImhvYW5nIiwiZ2l2ZW5fbmFtZSI6IiIsImZhbWlseV9uYW1lIjoiIiwiZW1haWwiOiJob2FuZ0BnbWFpbC5jb20ifQ.RKZtXWbOUtwMNCrF-R3h_c8dDD72eabnYwKWWwZL2XfdEeXjoKit7pBYiZBWzHqa8uR9zRMDmmWsh8joZVlPB1b7ra1d6mfvxQ0Vk18bzy2Wcbotw_2zn4MYyUHgKpJV2LYdCNcbvYuRl4QLVpWyW3mvnzh26xCJdgTQM2wl4bIcg_D6WQhmit69ih3uUEKBf4hgyopnb_cPX9keBjphNFxH1XHtt1SWbf9dSNCUy7NzrSWegbuqZemv4DBGiJalOFZDb15taUXmObvIIrC3OHsJhjnxVDK--RKWQ184dDyQI9h2zt5u_tYG4YDW5d1T6NVyW2ge9lbKOE084XF37Q"
    }
}

class DummyContext:
    function_name = "test_function"
    memory_limit_in_mb = 128
    invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test"
    aws_request_id = "test-id"

context = DummyContext()

@keycloak_token_required("test","test")
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": "Authorized access"
    }

if __name__ == "__main__":
    response = lambda_handler(event, context)
    print(response)