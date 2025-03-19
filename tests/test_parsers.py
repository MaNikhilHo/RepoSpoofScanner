from repospoofscanner.core.parsers import parse_package_json, parse_requirements_txt

def test_parse_package_json():
    content = """{"dependencies": {"lodash": "^4.0.0"}, "devDependencies": {"jest": "27.0.0"}}"""
    assert parse_package_json(content) == {"lodash": "^4.0.0", "jest": "27.0.0"}