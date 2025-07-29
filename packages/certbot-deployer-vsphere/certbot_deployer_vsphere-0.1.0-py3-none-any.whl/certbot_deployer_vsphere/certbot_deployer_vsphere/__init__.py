"""
VSphere Deployer
"""

import argparse
import logging
import os

from typing import ClassVar, Dict

import requests

from vmware.vapi.vsphere.client import (  # type:ignore
    VsphereClient,
    create_vsphere_client,
)
from com.vmware.vcenter.certificate_management.vcenter_client import Tls  # type:ignore

from certbot_deployer import Deployer, CertificateBundle, CertificateComponent
from certbot_deployer import CERT, INTERMEDIATES, KEY
from certbot_deployer import CERT_FILENAME, INTERMEDIATES_FILENAME, KEY_FILENAME
from certbot_deployer_vsphere.meta import __description__, __version__


def put_certificate(
    host: str,
    user: str,
    password: str,
    certificate_bundle: CertificateBundle,
    tls_no_verify: bool = False,
) -> None:
    """
    Install the certificates on the target
    """
    session: requests.Session = requests.session()
    if tls_no_verify:
        session.verify = False
    client: VsphereClient = create_vsphere_client(
        server=host, username=user, password=password, session=session
    )
    logging.debug("Authenticated to API")

    with open(certificate_bundle.cert.path, "r", encoding="utf-8") as cert_file, open(
        certificate_bundle.key.path, "r", encoding="utf-8"
    ) as key_file, open(
        certificate_bundle.intermediates.path, "r", encoding="utf-8"
    ) as intermediates_file:
        cert: str = cert_file.read()
        key: str = key_file.read()
        intermediates: str = intermediates_file.read()
    spec: Tls.Spec = Tls.Spec(cert=cert, key=key, root_cert=intermediates)
    client.vcenter.certificate_management.vcenter.Tls.set(spec)
    logging.debug("Certificate replaced successfully!")


class VsphereDeployer(Deployer):
    """
    vSphere deployer
    """

    subcommand: ClassVar[str] = "vsphere"
    version: ClassVar[str] = __version__

    @staticmethod
    def register_args(*, parser: argparse.ArgumentParser) -> None:
        """
        Register command-line arguments for the ExampleDeployer.
        """
        parser.description = __description__

        parser.add_argument(
            "--user",
            "-u",
            help=("vSphere API user"),
            required=True,
            type=str,
        )

        parser.add_argument(
            "--password",
            "-p",
            help=("vSphere API password"),
            required=True,
            type=str,
        )

        parser.add_argument(
            "--host",
            "-H",
            help=("vsphere host to target"),
            required=True,
            type=str,
        )

        parser.add_argument(
            "--tls-no-verify",
            action="store_true",
            default=False,
            help=(
                "Skip TLS verification of the API endpoints e.g. if deploying Certbot "
                "certificates over self-signed certificates currently in-place"
            ),
        )

    @staticmethod
    def entrypoint(
        *, args: argparse.Namespace, certificate_bundle: CertificateBundle
    ) -> None:
        """
        Execute the deployment process.
        """
        put_certificate(
            host=args.host,
            user=args.user,
            password=args.password,
            tls_no_verify=args.tls_no_verify,
            certificate_bundle=certificate_bundle,
        )
