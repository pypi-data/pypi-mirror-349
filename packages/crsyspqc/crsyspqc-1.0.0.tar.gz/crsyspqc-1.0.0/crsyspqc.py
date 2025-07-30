#! python3
# -*- coding: utf-8 -*-

# A Python interface to CryptoSys PQC

# crsyspqc.py
# $Date: 2025-05-21 09:05:00 $
# ************************** LICENSE *****************************************
# Copyright (C) 2024-25 David Ireland, DI Management Services Pty Limited.
# t/a CryptoSys <www.di-mgt.com.au> <www.cryptosys.net>
# This code is provided 'as-is' without any express or implied warranty.
# Free license is hereby granted to use this code as part of an application
# provided this license notice is left intact. You are *not* licensed to
# share any of this code in any form of mass distribution, including, but not
# limited to, reposting on other websites or in any source code repository.
# ****************************************************************************

# Requires `CryptoSys PQC` to be installed on your system,
# available from <https://www.cryptosys.net/pqc/>.

import platform
from ctypes import create_string_buffer, c_char_p, c_int

__version__ = "1.0.0.0000"
# History:
# [1.0.0] First Python interface to CryptoSys PQC


# OUR EXPORTED CLASSES
__all__ = (
    'Error',
    'General', 'Dsa', 'Kem', 'Rng', 'Util',
)

# Our global DLL/so-library object for CryptoSys PQC
if platform.system() == 'Windows':
    from ctypes import windll
    _didll = windll.diCrPQC
else:
    from ctypes import cdll
    _didll = cdll.LoadLibrary('libcrsyspqc.so')

# Global constants
_INTMAX = 2147483647
_INTMIN = -2147483648


class Error(Exception):
    """Raised when a call to a core PQC library function returns an error,
    or some obviously wrong parameter is detected."""

    # Google Python Style Guide: "The base exception for a module should be called Error."

    def __init__(self, value):
        """."""
        self.value = value

    @staticmethod
    def _isanint(v):
        try:
            v = int(v)
        except ValueError:
            pass
        return isinstance(v, int)

    def __str__(self):
        """Behave differently if value is an integer or not."""
        if (Error._isanint(self.value)):
            errcode = int(self.value)
            s1 = "ERROR CODE %d: %s" % (errcode, General.error_lookup(errcode))
        else:
            s1 = "ERROR: %s" % (self.value)
        return s1


class Dsa:
    """Digital Signature Algorithm (DSA) functions."""
    class Alg:
        """DSA signature algorithms."""
        ML_DSA_44: int = 0x20  #: ML-DSA-44 from FIPS.204 (based on Dilithium2)
        ML_DSA_65: int = 0x21  #: ML-DSA-65 from FIPS.204 (based on Dilithium3)
        ML_DSA_87: int = 0x22  #: ML-DSA-87 from FIPS.204 (based on Dilithium5)
        SLH_DSA_SHA2_128S: int = 0x32  #: SLH-DSA-SHA2-128s from FIPS.205
        SLH_DSA_SHA2_128F: int = 0x33  #: SLH-DSA-SHA2-128f from FIPS.205
        SLH_DSA_SHA2_192S: int = 0x34  #: SLH-DSA-SHA2-192s from FIPS.205
        SLH_DSA_SHA2_192F: int = 0x35  #: SLH-DSA-SHA2-192f from FIPS.205
        SLH_DSA_SHA2_256S: int = 0x36  #: SLH-DSA-SHA2-256s from FIPS.205
        SLH_DSA_SHA2_256F: int = 0x37  #: SLH-DSA-SHA2-256f from FIPS.205
        SLH_DSA_SHAKE_128S: int = 0x3A  #: SLH-DSA-SHAKE-128s from FIPS.205
        SLH_DSA_SHAKE_128F: int = 0x3B  #: SLH-DSA-SHAKE-128f from FIPS.205
        SLH_DSA_SHAKE_192S: int = 0x3C  #: SLH-DSA-SHAKE-192s from FIPS.205
        SLH_DSA_SHAKE_192F: int = 0x3D  #: SLH-DSA-SHAKE-192f from FIPS.205
        SLH_DSA_SHAKE_256S: int = 0x3E  #: SLH-DSA-SHAKE-256s from FIPS.205
        SLH_DSA_SHAKE_256F: int = 0x3F  #: SLH-DSA-SHAKE-256f from FIPS.205

    class SigOpts:
        """Signature options."""
        DEFAULT = 0  #: Default options.
        DETERMINISTIC = 0x2000  #: Use deterministic variant when signing [default = add randomness].
        INTERNAL = 0x4000000  #: Use ``Sign_internal`` or ``Verify_internal`` algorithm (for testing purposes).
        EXTERNAL_MU = 0x8000000  #: Use ``ExternalMu-ML-DSA.Sign`` or ``ExternalMu-ML-DSA.Verify`` algorithm (ML-DSA only).

    class PreHashAlg:
        """Hash function identifiers for pre-hash signing."""
        SHA256: int = 0x1  #: SHA-256 from FIPS.180-4
        SHA384: int = 0x2  #: SHA-284 from FIPS.180-4
        SHA512: int = 0x3  #: SHA-512 from FIPS.180-4
        SHA224: int = 0x4  #: SHA-224 from FIPS.180-4
        SHA512_224: int = 0x5  #: SHA-512/224 from FIPS.180-4
        SHA512_256: int = 0x6  #: SHA-512/256 from FIPS.180-4
        SHA3_224: int = 0x7  #: SHA3-224 from FIPS.202
        SHA3_256: int = 0x8  #: SHA3-256 from FIPS.202
        SHA3_384: int = 0x9  #: SHA3-384 from FIPS.202
        SHA3_512: int = 0xA  #: SHA3-512 from FIPS.202
        SHAKE128_256: int = 0xB  #: SHAKE-128-256 from FIPS.202
        SHAKE256_512: int = 0xC  #: SHAKE-256-512 from FIPS.202

    @staticmethod
    def keygen(alg, params=''):
        """Generate a DSA signing key pair (pk, sk).

        Args:
            alg (Dsa.Alg): Signature algorithm.
            params (str): Optional parameter to pass known test random material encoded in hexadecimal
                [default = add fresh randomness].
                For SLH-DSA pass a ``3*n`` value ``SK.seed||SK.prf||PK.seed`` (48/72/96 bytes).
                For ML-DSA pass a 32-byte value ``seed`` (denoted ξ in FIPS.204).

        Returns:
            bytes: Key pair.
        """
        flags = int(alg)
        n = _didll.DSA_KeyGen(None, 0, params.encode(), flags)
        if (n < 0): raise Error(-n)
        buf = create_string_buffer(n)
        n = _didll.DSA_KeyGen(buf, n, params.encode(), flags)
        if (n < 0): raise Error(-n)
        pksk = bytes(buf.raw)
        # Split pk||sk into separate byte arrays
        pklen = Dsa.publickey_size(alg)
        sklen = Dsa.privatekey_size(alg)
        return pksk[:pklen], pksk[-sklen:]

    @staticmethod
    def sign(alg, msg, privatekey, opts=SigOpts.DEFAULT, context=b'', params=''):
        """Generate a DSA signature over a message.

        Args:
            alg (Dsa.Alg): DSA algorithm.
            msg (bytes): Message to be signed.
            privatekey (bytes): Private key `sk`.
            opts (Dsa.SigOpts): Signature options.
            context(bytes): Optional context string (maximum 255 bytes)
            params (str): Optional parameter to pass known test random material *encoded in hexadecimal*
                [default = add fresh randomness if in hedged mode; else ignored].
                For SLH-DSA pass a value ``addrnd`` of exactly ``n`` bytes (16/24/32 bytes).
                For ML-DSA pass a 32-byte value ``rnd``.

        Returns:
            bytes: Signature value.

        Raises:
            Error: If parameters are bad, wrong lengths, etc.

        When using the ``ExternalMu-ML-DSA.Sign`` option (:py:attr:`Dsa.SigOps.EXTERNAL_MU`), pass the value of ``mu``
        instead of the message (ML-DSA only). This must be exactly 64 bytes long.
        Caller is responsible for computing the value of ``mu`` independently prior to input.

        For ML-DSA, the private key sk may be passed in expanded form (2560|4032|4896 bytes) or as a 32-byte seed.
        The key form is detected automatically by its length.
        """
        flags = int(alg) | int(opts)
        n = _didll.DSA_Sign(None, 0, msg, len(msg), privatekey, len(privatekey), context, len(context), params.encode(), flags)
        if (n < 0): raise Error(-n)
        buf = create_string_buffer(n)
        n = _didll.DSA_Sign(buf, n, msg, len(msg), privatekey, len(privatekey), context, len(context), params.encode(), flags)
        if (n < 0): raise Error(-n)
        return bytes(buf.raw)

    @staticmethod
    def sign_prehash(alg, msg, hashAlg, privatekey, opts=SigOpts.DEFAULT, context=b'', params=''):
        """Generate a DSA signature over a pre-hashed message.

        For the pre-hash variant, the hash digest of the message is passed instead of the message itself.
        Caller is responsible for computing the hash digest independently prior to input.
        The hash function used must be identifed in the ``hashAlg`` parameter.

        Args:
            alg (Dsa.Alg): DSA algorithm.
            msg (bytes): Hash digest of message to be signed ``PH_M = PH(M)``.
            hashAlg (Dsa.PreHashAlg): Pre-hash function used to create digest.
            privatekey (bytes): Private key `sk`.
            opts (Dsa.SigOpts): Signature options.
            context(bytes): Optional context string (maximum 255 bytes)
            params (str): Optional parameter to pass known test random material *encoded in hexadecimal*
                [default = add fresh randomness if in hedged mode; else ignored].
                For SLH-DSA pass a value ``addrnd`` of exactly ``n`` bytes (16/24/32 bytes).
                For ML-DSA pass a 32-byte value ``rnd``.

        Returns:
            bytes: Signature value.

        Raises:
            Error: If parameters are bad, wrong lengths, etc.

        For ML-DSA, the private key sk may be passed in expanded form (2560|4032|4896 bytes) or as a 32-byte seed.
        The key form is detected automatically by its length.
        """
        flags = int(alg) | int(opts)
        n = _didll.DSA_SignPreHash(None, 0, msg, len(msg), hashAlg, privatekey, len(privatekey), context, len(context), params.encode(), flags)
        if (n < 0): raise Error(-n)
        buf = create_string_buffer(n)
        n = _didll.DSA_SignPreHash(buf, n, msg, len(msg), hashAlg, privatekey, len(privatekey), context, len(context), params.encode(), flags)
        if (n < 0): raise Error(-n)
        return bytes(buf.raw)

    @staticmethod
    def verify(alg, signature, msg, publickey, context=b'', opts=SigOpts.DEFAULT):
        """Verify a DSA signature.

        Args:
            alg (Dsa.Alg): DSA algorithm.
            signature (bytes): Signature value
            msg (bytes): Message to be verified.
            publickey (bytes): Public key `pk`
            context(bytes): Same context string as used when signing (maximum 255 bytes).
            opts (Dsa.SigOpts): Verify options.

        Returns:
            bool: True if successfully verified or False if signature is invalid.

        Raises:
            Error: If parameters are bad, wrong lengths, etc.

        When using the ``ExternalMu-ML-DSA.Verify`` option (:py:attr:`Dsa.SigOps.EXTERNAL_MU`), pass the value of ``mu``
        instead of the message (ML-DSA only). This must be exactly 64 bytes long.
        Caller is responsible for computing the value of ``mu`` independently prior to input.

        """
        flags = int(alg) | int(opts)
        params = ''
        n = _didll.DSA_Verify(signature, len(signature), msg, len(msg), publickey, len(publickey), context, len(context), params.encode(), flags)
        # Catch straightforward invalid signature error
        _SIGNATURE_ERROR = -22
        if (n == _SIGNATURE_ERROR): return False
        # Raise error for other errors (bad params, missing file, etc.)
        if (n < 0): raise Error(-n)
        return True

    @staticmethod
    def verify_prehash(alg, signature, msg, hashAlg, publickey, context=b'', opts=SigOpts.DEFAULT):
        """Verify a DSA signature for a pre-hashed message.

        For the pre-hash variant, the hash digest of the message is passed instead of the message itself.
        Caller is responsible for computing the hash digest independently prior to input.
        The hash function used must be identifed in the ``hashAlg`` parameter.

        Args:
            alg (Dsa.Alg): DSA algorithm.
            signature (bytes): Signature value
            msg (bytes): Hash digest of message to be verified ``PH_M = PH(M)``.
            hashAlg (Dsa.PreHashAlg): Pre-hash function used to create digest.
            publickey (bytes): Public key `pk`
            context(bytes): Same context string as used when signing (maximum 255 bytes).
            opts (Dsa.SigOpts): Verify options.

        Returns:
            bool: True if successfully verified or False if signature is invalid.

        Raises:
            Error: If parameters are bad, wrong lengths, etc.
        """
        flags = int(alg) | int(opts)
        params = ''
        n = _didll.DSA_VerifyPreHash(signature, len(signature), msg, len(msg), hashAlg, publickey, len(publickey), context, len(context), params.encode(), flags)
        # Catch straightforward invalid signature error
        _SIGNATURE_ERROR = -22
        if (n == _SIGNATURE_ERROR): return False
        # Raise error for other errors (bad params, missing file, etc.)
        if (n < 0): raise Error(-n)
        return True

    @staticmethod
    def publickey_from_private(alg, privatekey):
        """Extract the public key from a private key.

        Args:
            alg (Dsa.Alg): DSA algorithm.
            privatekey (bytes): Private key `sk`.

        Returns:
            bytes: Public key `pk`.
        """
        flags = int(alg)
        n = _didll.DSA_PublicKeyFromPrivate(None, 0, privatekey, len(privatekey), flags)
        if (n < 0): raise Error(-n)
        buf = create_string_buffer(n)
        n = _didll.DSA_PublicKeyFromPrivate(buf, n, privatekey, len(privatekey), flags)
        if (n < 0): raise Error(-n)
        pk = bytes(buf.raw)
        return pk

    @staticmethod
    def publickey_size(alg):
        """Return length of public key in bytes for given algorithm.

        Args:
            alg (Dsa.Alg): Signature algorithm.

        Returns:
            int: length in bytes.

        Example:
            >>> Dsa.publickey_size(Dsa.Alg.SLH_DSA_SHA2_128F)
            32
        """
        n = _didll.DSA_PublicKeySize(int(alg))
        if (n < 0): raise Error(-n)
        return n

    @staticmethod
    def privatekey_size(alg):
        """Return length of private key in bytes for given algorithm.

        Args:
            alg (Dsa.Alg): Signature algorithm.

        Returns:
            int: length in bytes.

        Example:
            >>> Dsa.privatekey_size(Dsa.Alg.ML_DSA_65)
            4032
        """
        n = _didll.DSA_PrivateKeySize(int(alg))
        if (n < 0): raise Error(-n)
        return n

    @staticmethod
    def signature_size(alg):
        """Return length of signature in bytes for given algorithm.

        Args:
            alg (Dsa.Alg): Signature algorithm.

        Returns:
            int: length in bytes.

        Example:
            >>> Dsa.signature_size(Dsa.Alg.SLH_DSA_SHAKE_256F)
            49856
        """
        n = _didll.DSA_SignatureSize(int(alg))
        if (n < 0): raise Error(-n)
        return n

    @staticmethod
    def alg_name(alg):
        """Get the algorithm name from its Alg code.

        Args:
            alg (Dsa.Alg): Signature algorithm.

        Returns:
            str: Algorithm name.

        Example:
            >>> Dsa.alg_name(Dsa.Alg.SLH_DSA_SHAKE_256F)
            'SLH-DSA-SHAKE-256f'
            >>> Dsa.alg_name(Dsa.Alg.ML_DSA_65)
            'ML-DSA-65'
        """
        flags = int(alg)
        nchars = _didll.PQC_AlgName(None, 0, flags)
        buf = create_string_buffer(nchars + 1)
        _didll.PQC_AlgName(buf, nchars, flags)
        return buf.value.decode()


class Kem:
    """Key-Encapsulation Mechanism (KEM) functions."""

    class Alg:
        """Key-Encapsulation Mechanism (KEM) algorithms."""
        ML_KEM_512 = 0x10  #: ML_KEM_512 from FIPS.203 (based on Kyber512)
        ML_KEM_768 = 0x11  #: ML_KEM_768 from FIPS.203 (based on Kyber768)
        ML_KEM_1024 = 0x12  #: ML_KEM_1024 from FIPS.203 (based on Kyber1024)

    @staticmethod
    def keygen(alg, params=''):
        """Generate an encapsulation/decapsulation key pair (ek, dk).

        Args:
            alg (Kem.Alg): Kem algorithm.
            params (str): Optional parameter to pass known test random material of exactly
                64 bytes (``d||z``) encoded in hexadecimal [default=add fresh randomness].

        Returns:
            A key pair (ek, dk) both of type bytes.
        """
        flags = int(alg)
        n = _didll.KEM_KeyGen(None, 0, params.encode(), flags)
        if (n < 0): raise Error(-n)
        buf = create_string_buffer(n)
        n = _didll.KEM_KeyGen(buf, n, params.encode(), flags)
        if (n < 0): raise Error(-n)
        pksk = bytes(buf.raw)
        # Split ek||dk into separate byte arrays
        pklen = Kem.encapkey_size(alg)
        sklen = Kem.decapkey_size(alg)
        return pksk[:pklen], pksk[-sklen:]

    @staticmethod
    def encaps(alg, encapkey, params=''):
        """Carry out the ML-KEM encapsulation algorithm.

        Args:
            alg (Kem.Alg): Kem algorithm.
            encapkey (bytes): Encapsulation key `ek`
            params (str): Optional parameter to pass known test random material of exactly
                32 bytes (``m``) encoded in hexadecimal [default=add fresh randomness].

        Returns:
            A pair (ss, ct). Secret shared key `ss` and ciphertext `ct` both of type bytes.
        """
        flags = int(alg)
        n = _didll.KEM_Encaps(None, 0, encapkey, len(encapkey), params.encode(), flags)
        if (n < 0): raise Error(-n)
        buf = create_string_buffer(n)
        n = _didll.KEM_Encaps(buf, n, encapkey, len(encapkey), params.encode(), flags)
        if (n < 0): raise Error(-n)
        ssct = bytes(buf.raw)
        # Split ss||ct into separate byte arrays
        sslen = Kem.sharedkey_size(alg)
        ctlen = Kem.ciphertext_size(alg)
        return ssct[:sslen], ssct[-ctlen:]

    @staticmethod
    def decaps(alg, ct, decapkey):
        """Carry out the ML-KEM decapsulation algorithm.

        Args:
            alg (Kem.Alg): Kem algorithm.
            ct (bytes): Ciphertext `ct`
            decapkey (bytes): Decapsulation key `dk` (in expanded or 64-byte "seed" form)

        Returns:
            bytes: shared secret key, `ss`.
            On failure, `ss` will contain a pseudo-random value.
        """
        flags = int(alg)
        params = ''
        n = _didll.KEM_Decaps(None, 0, ct, len(ct), decapkey, len(decapkey), params.encode(), flags)
        if (n < 0): raise Error(-n)
        buf = create_string_buffer(n)
        n = _didll.KEM_Decaps(buf, n, ct, len(ct), decapkey, len(decapkey), params.encode(), flags)
        if (n < 0): raise Error(-n)
        return bytes(buf.raw)

    @staticmethod
    def encapkey_size(alg):
        """Return length in bytes of encapsulation key ("public key") for given algorithm.

        Args:
            alg (Kem.Alg): KEM algorithm.

        Returns:
            int: length in bytes.
        """
        n = _didll.KEM_EncapKeySize(int(alg))
        if (n < 0): raise Error(-n)
        return n

    @staticmethod
    def decapkey_size(alg):
        """Return length in bytes of expanded decapsulation key ("private key") for given algorithm.

        Args:
            alg (Kem.Alg): KEM algorithm.

        Returns:
            int: length in bytes.
        """
        n = _didll.KEM_DecapKeySize(int(alg))
        if (n < 0): raise Error(-n)
        return n

    @staticmethod
    def ciphertext_size(alg):
        """Return length in bytes of ciphertext `ct` for given algorithm.

        Args:
            alg (Kem.Alg): KEM algorithm.

        Returns:
            int: length in bytes.
        """
        n = _didll.KEM_CipherTextSize(int(alg))
        if (n < 0): raise Error(-n)
        return n

    @staticmethod
    def sharedkey_size(alg):
        """Return length in bytes of shared secret key `ss` for given algorithm.

        Args:
            alg (Kem.Alg): KEM algorithm.

        Returns:
            int: length in bytes.
        """
        n = _didll.KEM_SharedKeySize(int(alg))
        if (n < 0): raise Error(-n)
        return n

    @staticmethod
    def alg_name(alg):
        """Get the algorithm name from its Alg code.

        Args:
            alg (Kem.Alg): KEM algorithm.

        Returns:
            str: Algorithm name.

        Example:
            >>> Kem.alg_name(Kem.Alg.ML_KEM_768)
            'ML-KEM-768'
        """
        flags = int(alg)
        nchars = _didll.PQC_AlgName(None, 0, flags)
        buf = create_string_buffer(nchars + 1)
        nchars = _didll.PQC_AlgName(buf, nchars, flags)
        return buf.value.decode()


class General:
    """Get general info about the core DLL and errors returned by it."""

    @staticmethod
    def version():
        """Return the release version of the core CryptoSys PQC DLL as an integer value."""
        return _didll.PQC_Version()

    @staticmethod
    def module_name():
        """Return full path name of the current process's DLL module."""
        nchars = _didll.PQC_ModuleName(None, 0, 0)
        buf = create_string_buffer(nchars + 1)
        nchars = _didll.PQC_ModuleName(buf, nchars, 0)
        return buf.value.decode()

    @staticmethod
    def dll_info():
        """Get additional information about the core DLL module.

        Example:
            `Platform=X64;Compiled=May 24 2024 11:54:43;Licence=D`
        """
        nchars = _didll.PQC_DllInfo(None, 0, 0)
        buf = create_string_buffer(nchars + 1)
        nchars = _didll.PQC_DllInfo(buf, nchars, 0)
        return buf.value.decode()

    @staticmethod
    def error_lookup(n):
        """Return a description of an error code.

        Args:
            n (int): Code number

        Returns:
            str: Corresponding error message
        """
        nchars = 128
        buf = create_string_buffer(nchars + 1)
        _didll.PQC_ErrorLookup(buf, nchars, c_int(n))
        return buf.value.decode()


class Rng:
    """Random Number Generator to NIST SP800-90A."""

    # FIELDS
    SEED_BYTES = 128  #: Size in bytes of seed file.

    # CONSTANTS
    class Strength:
        """Required security strength for user-prompted entropy."""
        BITS_112 = 0  #: 112 bits of security
        BITS_128 = 1  #: 128 bits of security (default)
        BITS_192 = 2  #: 192 bits of security
        BITS_256 = 3  #: 256 bits of security

    class Opts:
        """RNG options."""
        DEFAULT = 0  #: Default option
        NO_INTEL_DRNG = 0x80000  #: Turn off support for Intel(R) DRNG for the current session.

    @staticmethod
    def bytestring(n):
        """Generate an array of n random bytes.

        Args:
            n (int): Required number of random bytes.

        Returns:
            bytes: Array of random bytes.
        """
        if (n < 0 or n > _INTMAX): raise Error('n out of range')
        buf = create_string_buffer(n)
        _didll.RNG_Bytes(buf, n, None, 0)
        return bytes(buf.raw)

    @staticmethod
    def initialize(seedfilename):
        """Initialize the RNG generator using a seed file.

        Use this function if Intel(R) DRNG is not available on your system
        (check using :py:func:`Rng.initialize_ex`).
        Call at the start of a session to load entropy stored in the seed file,
        and use again at the end of a session to save any accumulated entropy.
        If the seed file does not exist, it will be created using any available entropy.
        The seed file is automatically updated by this procedure.
        Use :py:func:`Rng.make_seedfile` to create the first time.

        Args:
            seedfilename (str): Full path name of seed file.

        Returns:
            int: Zero if successful.
        """
        n = _didll.RNG_Initialize(seedfilename.encode(), 0)
        if (n != 0): raise Error(-n if n < 0 else n)
        return n

    @staticmethod
    def initialize_ex(opts=0):
        """Query and initialize the RNG generator using Intel(R) DRNG, if available.

        Args:
            opts (Rng.Opts): Specify `Rng.Opts.NO_INTEL_DRNG` to explicitly *turn off* support.

        Returns:
            int: Support status for Intel(R) DRNG.
            If available, then returns a positive value 1 or greater; else a negative error code.
        """
        _PRNG_ERR_NOTAVAIL = -214
        flags = int(opts)
        n = _didll.RNG_Initialize("".encode(), flags)
        if (n < 0 and n != _PRNG_ERR_NOTAVAIL): raise Error(-n if n < 0 else n)
        return n

    @staticmethod
    def make_seedfile(seedfilename, strength=Strength.BITS_128, prompt=''):
        """Create a new seed file suitable for use with :py:func:`Rng.initialize`.

        This uses a dialog window and expects the user to type in random keystrokes.
        Such a GUI interface may not be appropriate in all circumstances.

        Args:
            seedfilename (str): Full path name of seed file to be created.
                Any existing file of the same name will be overwritten without warning.
            strength (Rng.Strength): Required security strength (default=128 bits).
            prompt (str): Optional prompt for dialog.

        Returns:
            int: Zero if successful.
        """
        n = _didll.RNG_MakeSeedFile(seedfilename.encode(), prompt.encode(), int(strength))
        if (n != 0): raise Error(-n if n < 0 else n)
        return n


class Util:
    """Utilities for strings, etc."""

    @staticmethod
    def substring(s, start, length):
        """Extract a substring of a string.

        Args:
            s (str): Source string.
            start (int): Start index (0 is the first character in the string). A negative value means count backwards from end of string.
            length (int): Length of substring to extract (specify 0 to indicate all characters to end of string).

        Returns:
            str: Extracted substring.
        """
        # NB we don't need this - Python has better slicing inbuilt
        # Just testing that the interface to the DLL works
        nc = len(s)
        buf = create_string_buffer(nc + 1)
        nc = _didll.UTIL_Substring(buf, nc, s.encode(), start, length)
        if (nc < 0): raise Error(-nc)
        return buf.value.decode()


class _NotUsed:
    """Dummy for parsing."""
    pass


# PROTOTYPES (derived from diCrPQC.h)
# If wrong argument type is passed, these will raise an `ArgumentError` exception
#     ArgumentError: argument 1: <type 'exceptions.TypeError'>: wrong type
_didll.PQC_Version.argtypes = []
_didll.PQC_ModuleName.argtypes = [c_char_p, c_int, c_int]
_didll.PQC_DllInfo.argtypes = [c_char_p, c_int, c_int]
_didll.PQC_ErrorLookup.argtypes = [c_char_p, c_int, c_int]
_didll.PQC_AlgName.argtypes = [c_char_p, c_int, c_int]
_didll.DSA_KeyGen.argtypes = [c_char_p, c_int, c_char_p, c_int]
_didll.DSA_Sign.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_didll.DSA_Verify.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_didll.DSA_SignPreHash.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_didll.DSA_VerifyPreHash.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_didll.DSA_PublicKeyFromPrivate.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_didll.DSA_PublicKeySize.argtypes = [c_int]
_didll.DSA_PrivateKeySize.argtypes = [c_int]
_didll.DSA_SignatureSize.argtypes = [c_int]
_didll.KEM_KeyGen.argtypes = [c_char_p, c_int, c_char_p, c_int]
_didll.KEM_Encaps.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_didll.KEM_Decaps.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_didll.KEM_EncapKeySize.argtypes = [c_int]
_didll.KEM_DecapKeySize.argtypes = [c_int]
_didll.KEM_CipherTextSize.argtypes = [c_int]
_didll.KEM_SharedKeySize.argtypes = [c_int]
_didll.UTIL_Substring.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_didll.RNG_Bytes.argtypes = [c_char_p, c_int, c_char_p, c_int]
_didll.RNG_Initialize.argtypes = [c_char_p, c_int]
_didll.RNG_InitializeEx.argtypes = [c_int]
_didll.RNG_MakeSeedFile.argtypes = [c_char_p, c_char_p, c_int]


def main():
    print("DLL version =", General.version())
    print(General.dll_info())
    print(General.module_name())
    s = General.error_lookup(6)
    print(s)
    for _ in range(3):
        b = Rng.bytestring(32)
        print(f"RNG={b.hex()}")
    pk, sk = Dsa.keygen(Dsa.Alg.SLH_DSA_SHA2_128F, "7C9935A0B07694AA0C6D10E4DB6B1ADD2FD81A25CCB148032DCD739936737F2DB505D7CFAD1B497499323C8686325E47")
    print(pk.hex(), sk.hex())


if __name__ == "__main__":
    main()
