=============================
The Hitchhiker's Guide to TLS
=============================

----------------
Create My Own CA
----------------

Example::

    $ openssl genrsa -des3 -out rootCA.key 2048
    $ openssl req -x509 -new -nodes -key rootCA.key -days 1024 -out rootCA.pem

--------------------
Create a Private Key
--------------------

Example::

    $ openssl genrsa -out example.key 2048

------------------------------------
Create a Certificate Signing Request
------------------------------------

Example::

    $ openssl req -new -key example.key -out example.csr

""""""""""""""""""""""""""""""""""""""""""""""""""
Create a CSR with Subject Alternative Names (SANs)
""""""""""""""""""""""""""""""""""""""""""""""""""

OpenSSL command line tools don't handle SANs in a particularly graceful
manner.  Don't panic!  The python wrapper script `generate_csr_with_san.py`
in this repository can take care of determining the options and creating
config files needed for you.  If you intend to use OpenSSL to sign the
CSR with your own CA (see below), you'll want to use the `-O` option to
preserve the OpenSSL config file that is generated, as it contains all
the extension and SAN information you'll need during signing. 

Example::

    $ ./generate_csr_with_san.py mydomain.key.pem mydomain.org -o ./mydomain.csr.pem -O mydomain.openssl.config

----------
Sign a CSR
----------

Example::

    $ openssl x509 -req -in example.csr \
        -CA rootCA.pem -CAkey rootCA.key -CAcreateserial \
        -out example.crt -days 500 -sha256

"""""""""""""""""""""""""""""""""""""""""
Sign a CSR with Subject Alternative Names
"""""""""""""""""""""""""""""""""""""""""

To include the SANs, you need to (1) enable the SAN extensions and (2) specify the SANs.
Both of these can be specified in the OpenSSL config file.  The command line just needs
to select the appropriate section::

    openssl x509 -req -in mydomain.csr.pem \
        -CA rootCA.pem -CAkey rootCA.key -CAcreateserial \
        -out mydomain.cert.pem -days 500 -sha256 \
        -extfile mydomain.openssl.config \
        -extensions v3_req

In the above command, the `-extfile` option spcifies a custom config file (see
`Create a CSR with Subject Alternative Names (SANs)` above).
The `-extensions` option indicates that the extensions in the "v3_req"
section should b used.  The rest of the configuration is in the config file
in various sections.

