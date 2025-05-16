"""
test_serve_file.py

Tests for the /files/<filename> endpoint.
"""

from tests.integration.helpers.utils import (create_dummy_file, 
                                             convert_file_endpoint, 
                                             serve_file_endpoint, get_case, 
                                             prepare_case_input, 
                                             assert_error_response)
from unittest.mock import patch

def test_200_case(client, settings):
    """"
    Happy path: successful file retrieval
    """

    testing_case = get_case("test_200_case")
    kwargs, output_filename_with_ext = prepare_case_input(settings, testing_case)
    create_dummy_file(kwargs["filepath"])

    response = convert_file_endpoint(client, **kwargs)

    response = serve_file_endpoint(client, output_filename_with_ext)

    assert response.status_code == 200
    assert response.headers["Content-Type"] in {"audio/wav", "audio/x-wav"}
    assert output_filename_with_ext in response.headers["Content-Disposition"] #to test that the file has correct name
    assert len(response.data) > 0
    response.close()


def test_404_case(client, settings):
    """
    Unhappy path: file not found
    """

    testing_case = get_case("test_route_not_found")
    kwargs, output_filename_with_ext = prepare_case_input(settings, testing_case)
    create_dummy_file(kwargs["filepath"])

    response = convert_file_endpoint(client, **kwargs)

    response = serve_file_endpoint(client, 'wrong_name' + output_filename_with_ext)

    assert_error_response(response, testing_case["status_code"], testing_case["custom_code"])
    response.close()



def test_internal_error(client, settings):
    """
    Simulates internal error while serving file
    """

    testing_case = get_case("test_internal_error")
    kwargs, output_filename_with_ext = prepare_case_input(settings, testing_case)
    
    create_dummy_file(kwargs["filepath"])

    response = convert_file_endpoint(client, **kwargs)
    with patch("app.api.routers.send_from_directory", side_effect=Exception("Simulated crash")):
        response = serve_file_endpoint(client, output_filename_with_ext)

    assert_error_response(response, testing_case["status_code"], testing_case["custom_code"])
    response.close()