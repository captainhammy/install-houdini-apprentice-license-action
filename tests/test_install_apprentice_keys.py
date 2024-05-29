"""Test the install_apprentice_keys script."""

# Standard Library
from argparse import Namespace

# install-houdini-apprentice-license-action
import install_apprentice_keys


def test_build_parser():
    """Test install_apprentice_keys.build_parser()."""
    parser = install_apprentice_keys.build_parser()

    expected = [action.dest for action in parser._actions[-2:]]

    assert expected == ["client_id", "client_secret"]


def test_get_keys_to_install(mocker):
    """Test install_apprentice_keys.get_keys_to_install()."""
    mock_keys = mocker.MagicMock(spec=dict)

    mock_service = mocker.MagicMock()
    mock_service.license.get_non_commercial_license.return_value = {"license_keys": mock_keys}

    mock_get_service = mocker.patch("install_apprentice_keys.sidefx.service", return_value=mock_service)

    mock_client_id = mocker.MagicMock(spec=str)
    mock_client_secret_key = mocker.MagicMock(spec=str)
    mock_server_name = mocker.MagicMock(spec=str)
    mock_server_code = mocker.MagicMock(spec=str)

    result = install_apprentice_keys.get_keys_to_install(
        mock_client_id,
        mock_client_secret_key,
        mock_server_name,
        mock_server_code,
    )

    assert result == mock_keys

    mock_get_service.assert_called_with(
        access_token_url=install_apprentice_keys.ACCESS_TOKEN_URL,
        client_id=mock_client_id,
        client_secret_key=mock_client_secret_key,
        endpoint_url=install_apprentice_keys.ENDPOINT_URL,
    )

    mock_service.license.get_non_commercial_license.assert_called_with(
        server_name=mock_server_name,
        server_code=mock_server_code,
        products=install_apprentice_keys.PRODUCTS_TO_INSTALL,
    )


def test_get_server_code(fp):
    """Test install_apprentice_keys.get_server_code()."""
    cmd_output = b"""----- SERVER localhost --------
SERVER localhost b1h255j9
sesinetd: Version 20.0.123
IP Address: fe80::d9d7:ed2c:cb0d:c9b8
Enabled Https: false
Read Mask:
Write Mask:
"""

    fp.register(["sesictrl", "print-server"], stdout=cmd_output)

    result = install_apprentice_keys.get_server_code()

    assert result == "b1h255j9"

    assert len(fp.calls) == 1


def test_install_licenses(fp):
    """Test install_apprentice_keys.install_licenses()."""
    licenses = [
        "aaa111",
        "bbb222",
        "ccc333",
    ]

    for license_key in licenses:
        fp.register(["sesictrl", "install", license_key])

    install_apprentice_keys.install_licenses(licenses)

    assert len(fp.calls) == len(licenses)


def test_main(mocker):
    """Test install_apprentice_keys.main()."""
    mock_namespace = mocker.MagicMock(spec=Namespace)
    mock_namespace.client_id = "test_id"
    mock_namespace.client_secret = "test_secret"

    mock_parser = mocker.patch("install_apprentice_keys.argparse.ArgumentParser")
    mock_parser.return_value.parse_args.return_value = mock_namespace

    mock_get_server_code = mocker.patch("install_apprentice_keys.get_server_code")
    mock_getfqdn = mocker.patch("socket.getfqdn")

    mock_get_keys = mocker.patch("install_apprentice_keys.get_keys_to_install")
    mock_install = mocker.patch("install_apprentice_keys.install_licenses")

    install_apprentice_keys.main()

    mock_get_keys.assert_called_with(
        "test_id",
        "test_secret",
        mock_getfqdn.return_value,
        mock_get_server_code.return_value,
    )

    mock_install.assert_called_with(mock_get_keys.return_value)
