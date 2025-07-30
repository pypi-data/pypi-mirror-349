from mcp import types
from mcp.server.fastmcp import FastMCP
from adfin_interaction import AdfinSession
from api_importer import load_apis
import sys

adfin = AdfinSession()
mcp = FastMCP("adfin")

@mcp.tool()
def upload_invoice_to_adfin(invoice_path: str) -> types.TextContent:
    """Upload an invoice to Adfin given its absolute path."""
    response = adfin.upload_invoice(invoice_path)
    return types.TextContent(type='text', text=response)

def register_all_apis():
    apis = load_apis()
    for api in apis:
        response_description = api["response_description"]

        clean_route = (api['route'].replace('/', '_').replace('-', '_').replace(':', '_')
                       .replace('{', '').replace('}', ''))

        if 'invoiceUpload' in clean_route:
            continue

        method_name = f'{api['method']}{clean_route}'
        clean_summary = api["summary"]
        if clean_summary is None:
            words = method_name.split('_')
            words[0] = words[0].capitalize()
            clean_summary = ' '.join(words) + '. '

        doc = clean_summary + '. '
        if response_description != "OK":
            doc += f'If successful, the outcome will be \"{api["response_description"]}\". '
        if api['request_data']:
            doc += f'The request data should be: {api["request_data"]}.'
        if api['parameters']:
            doc += f'The parameters should be: {api["parameters"]}.'
        else:
            doc += f'The request data should be an empty dictionary {{}}.'

# Claude is inconsistent in the way it provides a request_data that should be empty.
        method_str = f"""
@mcp.tool()
def {method_name}(request_data: dict = None) -> types.TextContent:
    \"\"\"{doc}\"\"\"
    print("The input of method {method_name} is", request_data, file=sys.stderr)
    if request_data is None or request_data == "" or request_data == "null" or request_data.get("request_data") == "null":
        request_data = None
    route = \"{api['route']}\"
    if '{{' in route:
        route = route.format(**request_data)
    response = adfin.call_route(\"{api['method']}\", route, request_data)
    print("The input of method {method_name} is", response, file=sys.stderr)
    return types.TextContent(type='text', text=str(response))
"""
        exec(method_str)

register_all_apis()


if __name__ == "__main__":
    mcp.run(transport='stdio')