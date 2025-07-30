from dimo.eth_signer import EthSigner
from dimo.errors import check_type, check_optional_type
from urllib.parse import urlencode
from typing import Dict, Optional
import json


class Auth:

    def __init__(self, request_method, get_auth_headers, env, dimo_instance):
        self._request = request_method
        self._get_auth_headers = get_auth_headers
        self.env = env
        self._dimo = dimo_instance

    def generate_challenge(
        self,
        client_id: str,
        domain: str,
        address: str,
        headers: Dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"},
        scope: str = "openid email",
        response_type: str = "code",
    ) -> Dict:
        check_type("client_id", client_id, str)
        check_type("domain", domain, str)
        check_type("address", address, str)
        if headers != {"Content-Type": "application/x-www-form-urlencoded"}:
            raise ValueError(
                "Headers must be '{'Content-Type': 'application/x-www-form-urlencoded'}'"
            )
        body = {
            "client_id": client_id,
            "domain": domain,
            "scope": scope,
            "response_type": response_type,
            "address": address,
        }

        response = self._request(
            "POST",
            "Auth",
            "/auth/web3/generate_challenge",
            data=urlencode(body),
            headers=headers,
        )
        
        if isinstance(response, bytes):
            response = json.loads(response.decode('utf-8'))
            
        return response

    def sign_challenge(self, message: str, private_key: str) -> str:
        check_type("message", message, str)
        check_type("private_key", private_key, str)

        return EthSigner.sign_message(message, private_key)

    def submit_challenge(
        self,
        client_id: str,
        domain: str,
        state: str,
        signature: str,
        headers: Dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"},
    ) -> Dict:
        check_type("client_id", client_id, str)
        check_type("domain", domain, str)
        check_type("state", state, str)
        check_type("signature", signature, str)
        check_type("headers", headers, dict)
        if headers != {"Content-Type": "application/x-www-form-urlencoded"}:
            raise ValueError(
                "Headers must be '{'Content-Type': 'application/x-www-form-urlencoded'}'"
            )

        form_data = {
            "client_id": client_id,
            "domain": domain,
            "state": state,
            "signature": signature,
            "grant_type": "authorization_code",
        }

        encoded_data = urlencode(form_data)

        response = self._request(
            "POST",
            "Auth",
            "/auth/web3/submit_challenge",
            data=encoded_data,
            headers=headers,
        )
        
        if isinstance(response, bytes):
            response = json.loads(response.decode('utf-8'))
            
        return response

    # Requires client_id, domain, and private_key. Address defaults to client_id.
    def get_dev_jwt(
        self,
        client_id: str,
        domain: str,
        private_key: str,
        address: Optional[str] = None,
        scope="openid email",
        response_type="code",
    ) -> Dict:
        """
        Generate a signed developer JWT in one step.
        For testing, mocks and POCs.

        Args:
            client_id (str): The Ethereum address of the client
            domain (str): The domain name for the client
            private_key (str): The private key to sign the challenge
        
        Returns:
            dict: The authentication response containing access_token
        """
        check_type("client_id", client_id, str)
        check_type("domain", domain, str)
        check_type("private_key", private_key, str)
        check_optional_type("address", address, str)

        self._dimo._client_id = client_id

        if address is None:
            address = client_id

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # Generate a challenge
        challenge = self.generate_challenge(
            headers=headers,
            client_id=client_id,
            domain=domain,
            scope=scope,
            response_type=response_type,
            address=address,
        )
        
        if isinstance(challenge, bytes):
            challenge = json.loads(challenge.decode('utf-8'))
        
        sign = self.sign_challenge(
            message=challenge["challenge"],
            private_key=private_key,
        )
        
        state = challenge["state"]
        signature = sign

        submit = self.submit_challenge(client_id, domain, state, signature, headers)
        
        if isinstance(submit, bytes):
            submit = json.loads(submit.decode('utf-8'))
            
        return submit
