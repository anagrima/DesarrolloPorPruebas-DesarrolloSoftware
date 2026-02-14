"""Module"""
import json
import os
import unittest

from freezegun import freeze_time
from uc3m_money import AccountManager
from uc3m_money import AccountManagementException


class MyDepositTest(unittest.TestCase):
    """ doc string de la clase"""
    @freeze_time("24/04/2025")
    def test1_valido(self):
        """ doc string del metodo"""
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test1_valido.json")
        try:
            with open(file_to_test, "r", encoding="utf8" )as archivo:
                datos = json.load(archivo)
                self.assertIn("IBAN", datos, "Exception: el archivo no contiene la clave IBAN")
                self.assertIn("AMOUNT", datos, "Exception: el archivo no contiene la clave AMOUNT")
        except FileNotFoundError:
            self.fail(f"Exception: el archivo {file_to_test} no existe")
        except json.JSONDecodeError:
            self.fail(f"Exception: el archivo {file_to_test} no tiene un formato JSON válido")

        my_manager = AccountManager()
        result = my_manager.deposit_into_acount(file_to_test)
        #comprobamos que devuelve la firma
        self.assertEqual(result, "6500af80a05d3356f8d39d490c213b0a225bf761b29f223e6538f91daf0251a4")
        #comrpobamos que deposit_store existe y que los datos insertados son correctos
        deposit_store_test =  os.path.join(os.path.dirname(__file__),
                                           "../../JsonFiles/RF2/deposit_store.json")
        try:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                deposits = json.load(archivo)
            iban_esperado = "ES3559005439021242088295"
            amount_esperado = "EUR 4321.35"
            deposit_encontrado = False
            for deposit in deposits:
                if deposit["to_iban"]==iban_esperado and deposit["deposit_amount"]==amount_esperado:
                    self.assertEqual(deposit["alg"], "SHA-256",
                                     "Exception: El algoritmo no es 'SHA-256'")
                    self.assertEqual(deposit["type"], "DEPOSIT",
                                     "Exception: El tipo de operación no es 'DEPOSIT'")
                    self.assertEqual(deposit["to_iban"], iban_esperado,
                                     "Exception: El IBAN no coincide")
                    self.assertEqual(deposit["deposit_amount"], amount_esperado,
                                     "Exception: El amount no coincide")
                    fecha_esperada = 1745452800.0 # Timestamp correspondiente a "24/04/2025"
                    self.assertEqual(deposit["deposit_date"], fecha_esperada,
                                     "Exception: La fecha no coincide")
                    self.assertEqual(deposit["deposit_signature"], result,
                                     "Exception: La firma no coincide")

                    deposit_encontrado = True
                    break
            if not deposit_encontrado:
                self.fail("Exception: el depósito no se ha guardado"
                          "de forma correcta en deposit_store.json")

        except FileNotFoundError:
            self.fail(f"Exception: el archivo {deposit_store_test} no existe")
        except json.JSONDecodeError:
            self.fail(f"Exception: el archivo {deposit_store_test} no tiene un formato JSON válido")

    def test2_f2_n1_del(self):
        """ doc string del metodo"""
        #no hay datos dentro del archivo de entrada json, no es un archivo con un formato válido
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test2_N1_DEL.json")
        #guardamos primero el contenido original del archivo deposits si es que
        # existe para luego comprobar que no se modifica
        #para todos los test seguiremos la misma estructura
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        #mensaje de error esperado
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        #ahora comprobamos que el deposit_store no se ha modificado si esque ya existía

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else: #si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test3_f2_n1_dup(self):
        """ doc string del metodo"""
        #los datos introducidos no siguen el formato json
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test3_N1_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = []

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test4_f2_n2_5_del(self):
        """ doc string del metodo"""
        # falta el primer corchete del objeto, el formato no es válido
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test4_N2_5_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message,
                         "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test5_f2_n2_5_dup(self):
        """ doc string del metodo"""
        # los datos introducidos no siguen el formato json
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test5_N2_5_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message,
                         "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test6_f2_n3_del(self):
        """ doc string del metodo"""
        #no hay datos en el archivo, por ello el primer error será que no encuentra la clave IBAN
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test6_N3_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message,
                         "Exception: nombre clave IBAN incorrecta")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test7_f2_n3_dup(self):
        """ doc string del metodo"""
        #los datos en el archivo se han duplicado, dos iban y dos amount
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test7_N3_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test8_f2_n4_9_del(self):
        """ doc string del metodo"""
        #el archivo no sigue un formato json
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test8_N4_9_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test9_f2_n4_9_dup(self):
        """ doc string del metodo"""
        # el archivo no sigue un formato json
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test9_N4_9_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test10_f2_n5_mod(self):
        """ doc string del metodo"""
        #El archivo no sigue un formato válido
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test10_N5_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")
    def test11_f2_n6_del(self):
        """ doc string del metodo"""
        # No existe el iban_field, por lo que primero hay una coma en el archivo, formato inválido
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test11_N6_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test12_f2_n6_dup(self):
        """ doc string del metodo"""
        # Hay dos iban_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test12_N6_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test13_f2_n7_del(self):
        """ doc string del metodo"""
        #Faltaría la coma separando las claves IBAN y AMOUNT
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test13_N7_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test14_f2_n7_dup(self):
        """ doc string del metodo"""
        # Hay dos comas separando las claves IBAN y AMOUNT
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test14_N7_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test15_f2_n7_mod(self):
        """ doc string del metodo"""
        # Modificamos la coma por el símbolo + separando las claves IBAN y AMOUNT
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test15_N7_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test16_f2_n8_del(self):
        """ doc string del metodo"""
        #Eliminamos el campo amount_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test16_N8_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test17_f2_n8_dup(self):
        """ doc string del metodo"""
        #Duplicamos el campo iban_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test17_N8_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test18_f2_n9_mod(self):
        """ doc string del metodo"""
        #modificamos el último corchete, formato no valido
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test18_N9_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test19_f2_n10_del(self):
        """ doc string del metodo"""
        #Eliminamos el nombre de la clave en iban_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test19_N10_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test20_f2_n10_dup(self):
        """ doc string del metodo"""
        # Duplicamos "IBAN", la clave en iban_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test20_N10_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test21_f2_n10_mod(self):
        """ doc string del metodo"""
        # Modificamos "IBAN" la clave en iban_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test21_N10_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test22_f2_n11_del(self):
        """ doc string del metodo"""
        #Eliminamos los dos puntos que separan la clave de su valor en iban_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test22_N11_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test23_f2_n11_dup(self):
        """ doc string del metodo"""
        # Duplicamos los dos puntos que separan la clave de su valor en iban_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test23_N11_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test24_f2_n11_mod(self):
        """ doc string del metodo"""
        # Modificamos los dos puntos que separan la clave de su valor en iban_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test24_N11_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test25_f2_n12_del(self):
        """ doc string del metodo"""
        #Eliminamos las primeras comillas del valor iban
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test25_N12_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test26_f2_n12_dup(self):
        """ doc string del metodo"""
        # Duplicamos las primeras comillas del valor iban
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test26_N12_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test27_f2_n12_mod(self):
        """ doc string del metodo"""
        # Modificamos las primeras comillas del valor iban
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test27_N12_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test28_f2_n13_del(self):
        """ doc string del metodo"""
        #Eliminamos el iban_value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test28_N13_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: el iban no es válido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test29_f2_n13_dup(self):
        """ doc string del metodo"""
        # Duplicamos el iban_value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test29_N13_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: el iban no es válido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test30_f2_n14_del(self):
        """ doc string del metodo"""
        # Eliminamos las segundas comillas del valor iban
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test30_N14_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test31_f2_n14_dup(self):
        """ doc string del metodo"""
        # Duplicamos las segundas comillas del valor iban
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test31_N14_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test32_f2_n14_mod(self):
        """ doc string del metodo"""
        # Modificamos las segundas comillas del valor iban
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test32_N14_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test33_f2_n15_del(self):
        """ doc string del metodo"""
        # Eliminamos el nombre de la clave de amount_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test33_N15_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test34_f2_n15_dup(self):
        """ doc string del metodo"""
        # Duplicamos el nombre de la clave en amount_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test34_N15_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test35_f2_n15_mod(self):
        """ doc string del metodo"""
        # Modificamos el nombre de la clave en amount_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test35_N15_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test36_f2_n16_del(self):
        """ doc string del metodo"""
        #Eliminamos los dos puntos que separan la clave de su valor en amount_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test36_N16_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test37_f2_n16_dup(self):
        """ doc string del metodo"""
        #Eliminamos los dos puntos que separan la clave de su valor en amount_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test37_N16_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")
    def test38_f2_n16_mod(self):
        """ doc string del metodo"""
        #Eliminamos los dos puntos que separan la clave de su valor en amount_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test38_N16_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test39_f2_n17_del(self):
        """ doc string del metodo"""
        #Eliminamos las primeras comillas de amount_value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test39_N17_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test40_f2_n17_dup(self):
        """ doc string del metodo"""
        #Duplicamos las primeras comillas de amount_value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test40_N17_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test41_f2_n17_mod(self):
        """ doc string del metodo"""
        #Modificamos las primeras comillas de amount_value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test41_N17_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test42_f2_n18_del(self):
        """ doc string del metodo"""
        #Eliminamos el campo amount_value, no hay ninguna cantidad introducida
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test42_N18_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test43_f2_n18_dup(self):
        """ doc string del metodo"""
        #Eliminamos el campo amount_value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test43_N18_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test44_f2_n19_del(self):
        """ doc string del metodo"""
        # Eliminamos las segundas comillas del valor amount
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test44_N19_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test45_f2_n19_dup(self):
        """ doc string del metodo"""
        #Duplicamos las segundas comillas del valor amount
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test45_N19_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test46_f2_n19_mod(self):
        """ doc string del metodo"""
        #Modificamos las segundas comillas del valor amount
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test46_N19_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")
    def test47_f2_n20_del(self):
        """ doc string del metodo"""
        #Eliminamos ES del iban_value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test47_N20_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: el iban no es válido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")
    def test48_f2_n20_dup(self):
        """ doc string del metodo"""
        #Duplicamos ES del iban_value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test48_N20_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: el iban no es válido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test49_f2_n20_mod(self):
        """ doc string del metodo"""
        #MOdificamos ES del iban_value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test49_N20_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: el iban no es válido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test50_f2_n21_24_del(self):
        """ doc string del metodo"""
        #Eliminamos el iban_num de iban_value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test50_N21_24_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: el iban no es válido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")
    def test51_f2_n21_24_dup(self):
        """ doc string del metodo"""
        #Duplicamos el iban_num de iban_value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test51_N21_24_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: el iban no es válido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test52_f2_n22_del(self):
        """ doc string del metodo"""
        #Eliminamos EUR del amount value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test52_N22_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test53_f2_n22_dup(self):
        """ doc string del metodo"""
        #Duplicamos EUR del amount value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test53_N22_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test54_f2_n22_mod(self):
        """ doc string del metodo"""
        #Modificamos EUR del amount value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test54_N22_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test55_f2_n23_del(self):
        """ doc string del metodo"""
        #Eliminamos el amount_num de amount value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test55_N23_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test56_f2_n23_dup(self):
        """ doc string del metodo"""
        #Duplicamos el amount_num de amount value
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test56_N23_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test57_f2_n24_mod(self):
        """ doc string del metodo"""
        #Modificamos el iban_num por valores numéricos cualquiera
        # que no cumplen con el algoritmo específico que se requiere
        #Anteriormente ya hemos comprobado que un iban válido se valida de forma correcta
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test57_N24_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: el iban no es válido")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test58_f2_n25_del(self):
        """ doc string del metodo"""
        #Eliminamos la parte entera de amount_num
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test58_N25_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test59_f2_n25_dup(self):
        """ doc string del metodo"""
        #Duplicamos la parte entera de amount_num
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test59_N25_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    @freeze_time("24/04/2025")
    def test60_f2_n25_mod(self):
        """ doc string del metodo"""
        #Modificamos la parte entera de amount
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test60_N25_MOD.json")
        try:
            with open(file_to_test, "r", encoding="utf8" )as archivo:
                datos = json.load(archivo)
                self.assertIn("IBAN", datos, "Exception: el archivo no contiene la clave IBAN")
                self.assertIn("AMOUNT", datos, "Exception: el archivo no contiene la clave AMOUNT")
        except FileNotFoundError:
            self.fail(f"Exception: el archivo {file_to_test} no existe")
        except json.JSONDecodeError:
            self.fail(f"Exception: el archivo {file_to_test} no tiene un formato JSON válido")

        my_manager = AccountManager()
        result = my_manager.deposit_into_acount(file_to_test)
        #comprobamos que devuelve la firma
        self.assertEqual(result, "f5c8aac96b5094e9b0f24ca5f686a2c3c5f4af7f7b6ad5eba54c122d1c7ce085")
        #comrpobamos que deposit_store existe y que los datos insertados son correctos
        deposit_store_test =  os.path.join(os.path.dirname(__file__),
                                           "../../JsonFiles/RF2/deposit_store.json")
        try:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                deposits = json.load(archivo)
            iban_esperado = "ES9121000418450200051332"
            amount_esperado = "EUR 1213.35"
            deposit_encontrado = False
            for deposit in deposits:
                if deposit["to_iban"]==iban_esperado and deposit["deposit_amount"]==amount_esperado:
                    self.assertEqual(deposit["alg"], "SHA-256",
                                     "Exception: El algoritmo no es 'SHA-256'")
                    self.assertEqual(deposit["type"], "DEPOSIT",
                                     "Exception: El tipo de operación no es 'DEPOSIT'")
                    self.assertEqual(deposit["to_iban"], iban_esperado,
                                     "Exception: El IBAN no coincide")
                    self.assertEqual(deposit["deposit_amount"], amount_esperado,
                                     "Exception: El amount no coincide")
                    fecha_esperada = 1745452800.0 # Timestamp correspondiente a "24/04/2025"
                    self.assertEqual(deposit["deposit_date"], fecha_esperada,
                                     "Exception: La fecha no coincide")
                    self.assertEqual(deposit["deposit_signature"], result,
                                     "Exception: La firma no coincide")

                    deposit_encontrado = True
                    break

            self.assertTrue(deposit_encontrado,
                            "Exception: el depósito no se ha"
                            "guardado de forma correcta en deposit_store.json")

        except FileNotFoundError:
            self.fail(f"Exception: el archivo {deposit_store_test} no existe")
        except json.JSONDecodeError:
            self.fail(f"Exception: el archivo {deposit_store_test} no tiene un formato JSON válido")

    def test61_f2_n26_del(self):
        """ doc string del metodo"""
        #Eliminamos el punto de amount_value que separa la parte decimal y entera
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test61_N26_DEL.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")


    def test62_f2_n26_dup(self):
        """ doc string del metodo"""
        #Duplicamos el punto de amount_num que divide la parte entera y decimal
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test62_N26_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test63_f2_n26_mod(self):
        """ doc string del metodo"""
        #Modificamos el punto de amount_num que divide la parte entera y decimal
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test63_N26_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    @freeze_time("24/04/2025")
    def test64_f2_n27_del(self):
        """ doc string del metodo"""
        #Eliminamos la parte decimal de amount_num, aunque se quede
        # como 4321. , segun hemos especificado, pueden no haber decimales, seguiría siendo válido
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test64_N27_DEL.json")
        try:
            with open(file_to_test, "r", encoding="utf8" )as archivo:
                datos = json.load(archivo)
                self.assertIn("IBAN", datos, "Exception: el archivo no contiene la clave IBAN")
                self.assertIn("AMOUNT", datos, "Exception: el archivo no contiene la clave AMOUNT")
        except FileNotFoundError:
            self.fail(f"Exception: el archivo {file_to_test} no existe")
        except json.JSONDecodeError:
            self.fail(f"Exception: el archivo {file_to_test} no tiene un formato JSON válido")

        my_manager = AccountManager()
        result = my_manager.deposit_into_acount(file_to_test)
        #comprobamos que devuelve la firma
        self.assertEqual(result, "c51317fa643ef585c67ee210355a8cf6e38190aa8eab402c4e0de4ea91ed4496")
        #comrpobamos que deposit_store existe y que los datos insertados son correctos
        deposit_store_test =  os.path.join(os.path.dirname(__file__),
                                           "../../JsonFiles/RF2/deposit_store.json")
        try:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                deposits = json.load(archivo)
            iban_esperado = "ES6211110783482828975098"
            amount_esperado = "EUR 4321."
            deposit_encontrado = False
            for deposit in deposits:
                if deposit["to_iban"]==iban_esperado and deposit["deposit_amount"]==amount_esperado:
                    self.assertEqual(deposit["alg"], "SHA-256",
                                     "Exception: El algoritmo no es 'SHA-256'")
                    self.assertEqual(deposit["type"], "DEPOSIT",
                                     "Exception: El tipo de operación no es 'DEPOSIT'")
                    self.assertEqual(deposit["to_iban"], iban_esperado,
                                     "Exception: El IBAN no coincide")
                    self.assertEqual(deposit["deposit_amount"], amount_esperado,
                                     "Exception: El amount no coincide")
                    fecha_esperada = 1745452800.0 # Timestamp correspondiente a "24/04/2025"
                    self.assertEqual(deposit["deposit_date"], fecha_esperada,
                                     "Exception: La fecha no coincide")
                    self.assertEqual(deposit["deposit_signature"], result,
                                     "Exception: La firma no coincide")

                    deposit_encontrado = True
                    break

            self.assertTrue(deposit_encontrado,
                            "Exception: el depósito no se ha guardado"
                            "de forma correcta en deposit_store.json")

        except FileNotFoundError:
            self.fail(f"Exception: el archivo {deposit_store_test} no existe")
        except json.JSONDecodeError:
            self.fail(f"Exception: el archivo {deposit_store_test} no tiene un formato JSON válido")

    def test65_f2_n27_dup(self):
        """ doc string del metodo"""
        #Duplicamos la parte decimal de amount_num
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test65_N27_DUP.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    @freeze_time("24/04/2025")
    def test66_f2_n27_mod(self):
        """ doc string del metodo"""
        #Modificamos la parte decimal de amount_num
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test66_N27_MOD.json")
        try:
            with open(file_to_test, "r", encoding="utf8" )as archivo:
                datos = json.load(archivo)
                self.assertIn("IBAN", datos, "Exception: el archivo no contiene la clave IBAN")
                self.assertIn("AMOUNT", datos, "Exception: el archivo no contiene la clave AMOUNT")
        except FileNotFoundError:
            self.fail(f"Exception: el archivo {file_to_test} no existe")
        except json.JSONDecodeError:
            self.fail(f"Exception: el archivo {file_to_test} no tiene un formato JSON válido")

        my_manager = AccountManager()
        result = my_manager.deposit_into_acount(file_to_test)
        #comprobamos que devuelve la firma
        self.assertEqual(result, "8d2c7c7235971cf287d69a33ed84d236d46f3afa7f84d9241916b7aee2ebba50")
        #comrpobamos que deposit_store existe y que los datos insertados son correctos
        deposit_store_test =  os.path.join(os.path.dirname(__file__),
                                           "../../JsonFiles/RF2/deposit_store.json")
        try:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                deposits = json.load(archivo)
            iban_esperado = "ES9121000418450200051332"
            amount_esperado = "EUR 4321.3"
            deposit_encontrado = False
            for deposit in deposits:
                if deposit["to_iban"]==iban_esperado and deposit["deposit_amount"]==amount_esperado:
                    self.assertEqual(deposit["alg"], "SHA-256",
                                     "Exception: El algoritmo no es 'SHA-256'")
                    self.assertEqual(deposit["type"], "DEPOSIT",
                                     "Exception: El tipo de operación no es 'DEPOSIT'")
                    self.assertEqual(deposit["to_iban"], iban_esperado,
                                     "Exception: El IBAN no coincide")
                    self.assertEqual(deposit["deposit_amount"], amount_esperado,
                                     "Exception: El amount no coincide")
                    fecha_esperada = 1745452800.0 # Timestamp correspondiente a "24/04/2025"
                    self.assertEqual(deposit["deposit_date"], fecha_esperada,
                                     "Exception: La fecha no coincide")
                    self.assertEqual(deposit["deposit_signature"], result,
                                     "Exception: La firma no coincide")

                    deposit_encontrado = True
                    break

            self.assertTrue(deposit_encontrado,
                            "Exception: el depósito no se ha guardado de"
                            "forma correcta en deposit_store.json")

        except FileNotFoundError:
            self.fail(f"Exception: el archivo {deposit_store_test} no existe")
        except json.JSONDecodeError:
            self.fail(f"Exception: el archivo {deposit_store_test} no tiene un formato JSON válido")

    # Test que no incluimos en el excel, pero, que vemos necesarios para
    # asegurar el correcto funcionamiento
    def test67_f2_n10_mod(self):
        """ doc string del metodo"""
        # Modificamos "IBAN" la clave en iban_field, test
        # repetido, pero sin modificar las comillas solo el
        # nombre de la clave, demostrando que aun asi también da error
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test67_N10_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: nombre clave IBAN incorrecta")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test68_f2_n15_mod(self):
        """ doc string del metodo"""
        # Modificamos el nombre de la clave en amount_field
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test68_N15_MOD.json")
        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = None

        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.deposit_into_acount(file_to_test)
        # mensaje de error esperado
        self.assertEqual(cm.exception.message, "Exception: nombre clave AMOUNT incorrecta")

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF2/deposit_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    @freeze_time("24/04/2025")
    def test69_f2_n26_del(self):
        """ doc string del metodo"""
        file_to_test = os.path.join(os.path.dirname(__file__),
                                    "../../JsonFiles/RF2/test69_n26_del.json")
        try:
            with open(file_to_test, "r", encoding="utf8" )as archivo:
                datos = json.load(archivo)
                self.assertIn("IBAN", datos, "Exception: el archivo no contiene la clave IBAN")
                self.assertIn("AMOUNT", datos, "Exception: el archivo no contiene la clave AMOUNT")
        except FileNotFoundError:
            self.fail(f"Exception: el archivo {file_to_test} no existe")
        except json.JSONDecodeError:
            self.fail(f"Exception: el archivo {file_to_test} no tiene un formato JSON válido")

        my_manager = AccountManager()
        result = my_manager.deposit_into_acount(file_to_test)
        #comprobamos que devuelve la firma
        self.assertEqual(result, "c015c235d4acf5a87da9d4a436a7f0401537c7141a013c9de9e390e40a4da847")
        #comrpobamos que deposit_store existe y que los datos insertados son correctos
        deposit_store_test =  os.path.join(os.path.dirname(__file__),
                                           "../../JsonFiles/RF2/deposit_store.json")
        try:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                deposits = json.load(archivo)
            iban_esperado = "ES9121000418450200051332"
            amount_esperado = "EUR 2135"
            deposit_encontrado = False
            for deposit in deposits:
                if deposit["to_iban"]==iban_esperado and deposit["deposit_amount"]==amount_esperado:
                    self.assertEqual(deposit["alg"], "SHA-256",
                                     "Exception: El algoritmo no es 'SHA-256'")
                    self.assertEqual(deposit["type"], "DEPOSIT",
                                     "Exception: El tipo de operación no es 'DEPOSIT'")
                    self.assertEqual(deposit["to_iban"], iban_esperado,
                                     "Exception: El IBAN no coincide")
                    self.assertEqual(deposit["deposit_amount"], amount_esperado,
                                     "Exception: El amount no coincide")
                    fecha_esperada = 1745452800.0 # Timestamp correspondiente a "24/04/2025"
                    self.assertEqual(deposit["deposit_date"], fecha_esperada,
                                     "Exception: La fecha no coincide")
                    self.assertEqual(deposit["deposit_signature"], result,
                                     "Exception: La firma no coincide")

                    deposit_encontrado = True
                    break

            self.assertTrue(deposit_encontrado,
                            "Exception: el depósito no se ha guardado de "
                            "forma correcta en deposit_store.json")

        except FileNotFoundError:
            self.fail(f"Exception: el archivo {deposit_store_test} no existe")
        except json.JSONDecodeError:
            self.fail(f"Exception: el archivo {deposit_store_test} no tiene un formato JSON válido")


if __name__ == '__main__':
    unittest.main()
