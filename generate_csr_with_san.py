#! /usr/bin/env python

from __future__ import print_function
import argparse
import subprocess
import tempfile
from textwrap import dedent

def main(args):
    config_preamble = dedent("""\
        [req]
        req_extensions = v3_req
        distinguished_name = req_distinguished_name
         
        [ req_distinguished_name ]
        countryName     = Country Name (2 letter code)
        countryName_default   = AU
        countryName_min     = 2
        countryName_max     = 2
        stateOrProvinceName   = State or Province Name (full name)
        stateOrProvinceName_default = Some-State
        localityName      = Locality Name (eg, city)
        0.organizationName    = Organization Name (eg, company)
        0.organizationName_default  = Internet Widgits Pty Ltd
        organizationalUnitName    = Organizational Unit Name (eg, section)
        commonName      = Common Name (e.g. server FQDN or YOUR name)
        commonName_max      = 64
        emailAddress      = Email Address
        emailAddress_max    = 64

        [ v3_req ]
        # Extensions to add to a certificate request
        basicConstraints = CA:FALSE
        keyUsage = nonRepudiation, digitalSignature, keyEncipherment
        subjectAltName = @alt_names

        [alt_names]
        """)
    private_key = args.private_key
    subjects = [args.subject]
    if args.san is not None:
        subjects.extend(args.san)
    config_subjects = '\n'.join(
        ["DNS.{0} = {1}".format(n, subj) 
            for n, subj in enumerate(subjects)])
    config = config_preamble + config_subjects
    print(config)
    print("")
    with tempfile.NamedTemporaryFile(bufsize=0) as config_file:
        config_file.write(config)
        cmd = [
            "openssl",
            "req",
            "-new",
            "-sha256",
            "-key",
            private_key,
            "-extensions",
            "v3_req",
            "-config",
            config_file.name,
        ]
        if args.outfile is not None:
            cmd.extend([
                "-out",
                args.outfile,
            ])
        #print(' '.join(cmd))
        print(" ".join(cmd))
        subprocess.check_output(cmd)
    if args.config_outfile is not None:
        with open(args.config_outfile, "w") as f:
            f.write(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Make Certificate Signing Requests (CSRs) with Subjet Alternative Names (SANs).")
    parser.add_argument(
        "private_key",
        action="store",
        help="The private key.")
    parser.add_argument(
        "subject",
        action="store",
        help="The subject of the certificate.")
    parser.add_argument(
        "-s",
        "--san",
        action="append",
        help="Subject alternative name.  May be specified multiple times.")
    parser.add_argument(
        "-o",
        "--outfile",
        action="store",
        help="Output file.")
    parser.add_argument(
        "-O",
        "--config-outfile",
        action="store",
        help="Store the intermediate config output file as CONFIG_OUTFILE.")
    args = parser.parse_args()
    main(args)
