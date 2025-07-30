import sys

import requests


def download_api_documentation(url='https://app.adfin.com/api/docs/Public-APIs'):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json(), True
    else:
        message = f"Error: {response.status_code} {response.text}"
        print(message, file=sys.stderr)
        return {'code': response.status_code, 'message': message}, False


def load_apis():
    loaded, success = download_api_documentation()
    if not success:
        raise Exception("Failed to download API documentation")
    paths = loaded['paths']
    components = loaded['components']['schemas']
    method_data = []
    for path, methods in paths.items():
        for method_name, method in methods.items():
            summary = method.get('summary')  # might be null
            success_code = '200'
            if success_code not in method['responses']:
                success_code = [e for e in method['responses'] if e.startswith('2')]
                if len(success_code) == 0:
                    success_code = [e for e in method['responses'] if e.startswith('3')][0]
                else:
                    success_code = success_code[0]
            response_description = method['responses'][success_code]['description']
            request_body = method.get('requestBody')
            request_data = None

            if request_body:
                content = request_body['content']
                data_type = list(content.keys())[0]
                schema = content[data_type]['schema']
                properties = schema.get('properties')
                if properties:
                    request_data = {key: value.get('description') for key, value in properties.items()}
                else:
                    if 'type' in schema and 'description' in schema:
                        request_data = {schema['type']: schema['description']}
                    else:
                        for key, value in schema.items():
                            if key == '$ref':
                                value = value.split('/')[-1]
                                request_data = components[value]['properties']
                            else:
                                raise ValueError(f"Unknown key: {key}")

            # Parameters parsing (query/path)
            request_params = method.get('parameters', [])
            parameters_data = []
            for param in request_params:
                param_schema = param.get('schema', {})
                parameters_data.append({
                    'name': param.get('name', 'Unnamed'),
                    'location': param.get('in', 'unknown'),  # "query" or "path"
                    'required': param.get('required', False),
                    'type': param_schema.get('type', 'unknown'),
                    'description': param.get('description', 'No description provided')
                })

            method_data.append({
                'route': path,
                'method': method_name,
                'summary': summary,
                'response_description': response_description,
                'request_data': request_data,
                'parameters': parameters_data
            })

    return method_data


if __name__ == '__main__':
    load_apis()
