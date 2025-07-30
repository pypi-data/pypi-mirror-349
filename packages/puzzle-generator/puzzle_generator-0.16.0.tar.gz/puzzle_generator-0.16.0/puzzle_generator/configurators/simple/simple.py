import typing

from ...encryption_algorithms.simple import simple as se
from . import cfs_common as csc
from ..check_kwargs import check_kwargs


class Simple:
    def __init__(self, **kwargs) -> None:
        check_kwargs({"scrypt_params", "signature_params"}, **kwargs)
        self._scrypt_params = csc.scrypt_params(**kwargs)
        self._signature_params = csc.signature_params(**kwargs)

    def get_modules(self) -> list[str]:
        return csc.MODULES

    def get_encrypt(self) -> typing.Callable[[bytes, bytes], bytes]:
        return se.get_encrypt(self._scrypt_params, self._signature_params)

    def get_needed_objects(self):
        return csc.OBJECTS + [
            se.get_decrypt,
        ]

    def get_constants_str(
        self,
    ) -> str:
        _scrypt_params = csc.scrypt_params_to_code_str(**self._scrypt_params)
        _signature_params = "_SIGNATURE_PARAMS = " + repr(self._signature_params)
        decrypt: str = "_DECRYPT = get_decrypt(_SCRYPT_PARAMS, _SIGNATURE_PARAMS)"
        return "\n".join([_scrypt_params, _signature_params, decrypt])
