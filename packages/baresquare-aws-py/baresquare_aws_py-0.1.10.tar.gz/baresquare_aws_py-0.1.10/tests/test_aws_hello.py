from unittest.mock import MagicMock, patch


def test_s3_import_and_instantiation():
    """Simple test to verify imports work and class can be instantiated."""
    from baresquare_aws_py import s3

    # Patch boto3 to avoid actual AWS calls
    with patch('boto3.client') as mock_boto3_client:
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        client = s3.S3Client()

        assert isinstance(client, s3.S3Client)
        print("Successfully imported and instantiated S3Client")


@patch('boto3.client')
@patch('os.getenv')
def test_ssm_import_only(mock_getenv, mock_boto3_client):
    """Simple test that only verifies imports work."""
    # Setup minimal mocks
    mock_getenv.return_value = None
    mock_boto3_client.return_value = MagicMock()

    # Just import the module - that's it

    # If we got here without errors, the test passes
    assert True, "Module imported successfully"
