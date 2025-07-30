Python for CryptoSys PQC
===================================

This is a Python interface to the **CryptoSys PQC** library <https://www.cryptosys.net/pqc>. 


**CryptoSys PQC** provides the three Post-Quantum Cryptography (PQC) algorithms specified by NIST in August 2024 
considered to be secure against an attack by a large-scale quantum computer. These are

- *Module-Lattice-Based Key-Encapsulation Mechanism* (ML-KEM) specified in FIPS.203,
- *Module-Lattice-Based Digital Signature Algorithm* (ML-DSA) specified in FIPS.204, and
- *Stateless Hash-based Digital Signature Algorithm* (SLH-DSA) specified in FIPS.205. 

All keys, signatures and ciphertext values in this library are input and output as byte arrays.

Known random values can be input to validate against test vectors.

For the DSA algorithms, options are provided to use the deterministic or hedged modes, to add a context string, and to use the pre-hash modes
HashML-DSA and HashSLH-DSA. For ML-DSA, there is the option to use the ExternalMu-ML-DSA algorithm, passing ``mu`` as the message.

For ML-DSA and ML-KEM, the private key can be passed in expanded or "seed" form (the form is automatically detected by the length).

Requires: Python 3.
CryptoSys PQC v1.0 or above must be installed on your system.
This is available from

    https://www.cryptosys.net/pqc


To use in Python's REPL
-----------------------

Using wild import for simplicity.

.. code-block:: python

    >>> from crsyspqc import *  # @UnusedWildImport
    >>> General.version() # "hello world!" for CryptoSys PQC
    10000
    >>> Dsa.privatekey_size(Dsa.Alg.ML_DSA_65)
    4032

The stricter way using the ``crsyspqc`` prefix.

.. code-block:: python

    >>> import crsyspqc
    >>> crsyspqc.General.version() # Underlying core CryptoSys PQC dll
    10000
    >>> crsyspqc.__version__  # crsyspqc.py module version
    '1.0.0.0000'
    >>> crsyspqc.Dsa.signature_size(crsyspqc.Dsa.Alg.SLH_DSA_SHAKE_256F)
    49856

Note that ``crsyspqc.General.version()`` gives the version number of the underlying core (native) CryptoSys PQC DLL, 
and ``crsyspqc.__version__`` gives the version of the Python crsyspqc module. 

Examples
--------

There is a series of tests in ``test_crsyspqc.py`` (`source <https://www.cryptosys.net/pqc/test_crsyspqc.py.html>`_).
You should find an example there of what you want to do.


Contact
-------

For more information or to make suggestions, please contact us at
https://www.cryptosys.net/contact/

| David Ireland
| DI Management Services Pty Ltd t/a CryptoSys
| Australia
| <https://www.di-mgt.com.au> <https://www.cryptosys.net>
| 21 May 2025
