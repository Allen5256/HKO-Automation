import json
import allure

def attach_text(name, content):
    allure.attach(content, name=name, attachment_type=allure.attachment_type.TEXT)

def attach_json(name, obj):
    try:
        pretty = json.dumps(obj, indent=2, ensure_ascii=False)
    except Exception:
        pretty = str(obj)
    allure.attach(pretty, name=name, attachment_type=allure.attachment_type.JSON)

def attach_kv(title, mapping):
    lines = [f"{k}: {v}" for k, v in mapping.items()]
    attach_text(title, "\n".join(lines))

def attach_screenshot(driver, name= "screenshot"):
    png = driver.get_screenshot_as_png()
    allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)

def attach_request_response(request_name, method, url, req_headers, req_body, status_code, resp_headers, resp_body):
    attach_kv(f"{request_name} - Request", {"method": method, "url": url})
    if req_headers:
        attach_json(f"{request_name} - Request Headers", req_headers)
    if req_body is not None:
        attach_json(f"{request_name} - Request Body", req_body)
    attach_kv(f"{request_name} - Response Meta", {"status_code": status_code})
    if resp_headers:
        attach_json(f"{request_name} - Response Headers", dict(resp_headers))
    if resp_body is not None:
        attach_json(f"{request_name} - Response Body", resp_body)
