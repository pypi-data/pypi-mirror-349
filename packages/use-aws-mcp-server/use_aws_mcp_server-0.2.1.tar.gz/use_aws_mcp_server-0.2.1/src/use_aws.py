import uuid

from mcp.server.fastmcp import FastMCP
from strands_tools import use_aws as strands_tools_use_aws

mcp = FastMCP("use-aws-mcp-server")


@mcp.tool()
def use_aws(
    region: str,
    service_name: str,
    operation_name: str,
    label: str,
    parameters: dict = {},
    profile_name: str = None,
):
    """
    Make an AWS CLI api call with the specified service, operation, and parameters. All arguments MUST conform to the AWS CLI specification. Should the output of the invocation indicate a malformed command, invoke help to obtain the the correct command.

    Args:
        region (str): Region name for calling the operation on AWS.
        service_name (str): The name of the AWS service. If you want to query s3, you should use s3api if possible.
        operation_name (str): The name of the operation to perform. You should also prefer snake case.
        label (str): Human readable description of the api that is being called.
        parameters (dict): The parameters for the operation. The parameter keys MUST conform to the AWS CLI specification. You should prefer to use JSON Syntax over shorthand syntax wherever possible. For parameters that are booleans, prioritize using flags with no value. Denote these flags with flag names as key and an empty string as their value. You should also prefer kebab case.
        profile_name (str): Optional: AWS profile name to use from ~/.aws/credentials. Defaults to default profile if not specified.
    """

    tool_use_id = str(uuid.uuid4())[:8]
    name = "use_aws"

    input_dict = {
        "service_name": service_name,
        "operation_name": operation_name,
        "region": region,
        "label": label,
    }

    if parameters is not None:
        input_dict["parameters"] = parameters
    if profile_name is not None:
        input_dict["profile_name"] = profile_name

    result = strands_tools_use_aws.use_aws(
        {
            "toolUseId": tool_use_id,
            "name": name,
            "input": input_dict,
        }
    )

    return result["content"][0]["text"]

def main():
    mcp.run()

if __name__ == "__main__":
    main()
