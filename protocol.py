from dataclasses import dataclass
from typing import Optional, Dict, Any
import json


## Data Models

# data container for any protocol errors
@dataclass
class JSONRPCError:
    code: int
    message: str
    data: Optional[Any] = None

    # to_dict function, omitting data if None -- serializes data into format for converting to JSON later
    def to_dict(self) -> Dict[str, Any]:
        error: Dict[str, Any] = {
            "code": self.code,
            "message": self.message,
        }

        if self.data is not None:
            error["data"] = self.data

        return error
        


# data container to store incoming JSON RPC requests from mcp host
@dataclass
class JSONRPCRequest:
    id: str | int
    method: str
    params: Optional[Dict[str, Any]] = None
    jsonrpc: str = "2.0" # version of jsonrpc format being used

    def to_dict(self) -> Dict[str, Any]:
        request: Dict[str, Any] = {
            "id": self.id,
            "method": self.method,
            "jsonrpc": self.jsonrpc,
        }

        if self.params is not None:
            request["params"] = self.params

        return request


# data container to store notifications about status of mcp client-server connection
@dataclass
class JSONRPCNotification:
    method: str
    params: Optional[Dict[str, Any]] = None
    jsonrpc: str = "2.0"

    def to_dict(self) -> Dict[str, Any]:
        notification: Dict[str, Any] = {
            "method": self.method,
            "jsonrpc": self.jsonrpc,
        }

        if self.params is not None:
            notification["params"] = self.params

        return notification


# data container to construct response back to mcp host (only constructed by mcp server)
@dataclass
class JSONRPCResponse:
    id: Optional[str | int]
    result: Optional[Any] = None
    error: Optional[JSONRPCError] = None
    jsonrpc: str = "2.0"

    def to_dict(self) -> Dict[str, Any]:

        # Enforce JSON-RPC constraint: mutually exclusive result and error (cannot have both result and error)
        if self.result is not None and self.error is not None:
            raise ValueError("JSONRPCResponse cannot contain both 'result' and 'error'")

        # Enforce JSON-RPC constraint: at least one of result or error must be non None
        if self.result is None and self.error is None:
            raise ValueError("JSONRPCResponse must contain either 'result' or 'error'")

        response: Dict[str, Any] = {
            "jsonrpc": self.jsonrpc,
            "id": self.id
        }

        if self.error is not None:
            response["error"] = self.error.to_dict()
        else:
            response["result"] = self.result

        return response



# deserialize function that accepts incoming data from mcp host, parsing the json payload and deserializing it into Python objects (one of objects above)
def parse_json(raw_json: str) -> JSONRPCRequest | JSONRPCNotification | JSONRPCError:
    """
        Parses and validates a raw JSON-RPC text string into a typed protocol object.
    """
    try:
        payload = json.loads(raw_json)

        if not isinstance(payload, dict):
            return JSONRPCError(code=-32600, message="Invalid Request: Payload must be a JSON object")

        if "jsonrpc" not in payload or payload["jsonrpc"] != "2.0":
            return JSONRPCError(code=-32600, message="Invalid Request: Must be a JSON-RPC 2.0 object")
        
        if "method" not in payload or not isinstance(payload["method"], str):
            return JSONRPCError(code=-32600, message="Invalid Request: Missing or malformed 'method'")

        # Request if payload contains "id"
        if "id" in payload:
            return JSONRPCRequest(id=payload["id"],
                                  method=payload["method"],
                                  params=payload.get("params"), # returns None if does not exist
                                  jsonrpc=payload["jsonrpc"])
        # Notification otherwise  
        else:
            return JSONRPCNotification(method=payload["method"],
                                       params=payload.get("params"),
                                       jsonrpc=payload["jsonrpc"])

    except json.JSONDecodeError:
        return JSONRPCError(code=-32700, message="Parse error")
