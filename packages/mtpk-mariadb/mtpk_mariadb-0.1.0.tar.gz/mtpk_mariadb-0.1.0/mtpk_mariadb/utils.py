#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
# ----------------------------------------
# jjandres 2025 - 17-05-2025)
# ----------------------------------------
# pylint: disable=multiple-imports
# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace
# pylint: disable=wrong-import-position
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=unused-argument
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=unused-variable
# pylint: disable=bare-except
# pylint: disable=protected-access
# pylint: disable=ungrouped-imports
# pylint: disable=wrong-import-order
# pylint: disable=redefined-builtin
# pylint: disable=unidiomatic-typecheck
# pylint: disable=singleton-comparison
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-lines
# pylint: disable=anomalous-backslash-in-string
# pylint: disable=broad-except
# pylint: disable=too-many-arguments
# pylint: disable=broad-exception-raised
# pylint: disable=consider-using-f-string
# 
 

import bcrypt

def hash_password(plain_password: str) -> str:
    """
    Genera un hash seguro de una contraseña en texto plano.

    Args:
        plain_password (str): Contraseña original en texto plano.

    Returns:
        str: Hash seguro (en formato string) listo para almacenar en la base de datos.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode(), salt)
    return hashed.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash almacenado.

    Args:
        plain_password (str): Contraseña introducida por el usuario.
        hashed_password (str): Hash previamente almacenado.

    Returns:
        bool: True si coinciden, False si no.
    """
    return bcrypt.checkpw(
        plain_password.encode(), 
        hashed_password.encode()
    )
