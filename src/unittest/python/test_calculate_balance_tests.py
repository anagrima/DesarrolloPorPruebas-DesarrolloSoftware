""" doc string del metodo"""
import os
import unittest
import json
from datetime import datetime

from uc3m_money import AccountManager
from uc3m_money import AccountManagementException


class MyTestBalanceCase(unittest.TestCase):
    """ doc string de la clase"""
    def test1_valid(self):
        """doc string del metodo"""
        # iban es correcto y coincide con algunos de los transactions, comprobamos
        # que los resultados son los esperados
        iban = "ES8658342044541216872704"
        my_manager = AccountManager()
        # guardamos primero el contenido del archivo original de transactions para
        # asegurarnos de que no se cambia nada
        # seguiremos este proceso a lo largo de todos los test, comrpobando asi
        # si se cambia o no el contenido del archivo
        transactions_test = os.path.join(os.path.dirname(__file__),
                                         "../../JsonFiles/RF3/transactions.json")

        if os.path.exists(transactions_test):
            with open(transactions_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = []

        # calculamos el resultado que deberá de dar este balance con este iban y comparamos
        balance = 0
        for transaccion in contenido_org:
            if transaccion["IBAN"] == iban:
                balance += float(transaccion["amount"])

        date = datetime.now().strftime("%d/%m/%Y")
        #la línea print la usábamos para asegurarnos de que las cantidades coincidían
        #print(f"Balance calculado a partir de deposit_store: {balance})
        # primero comprobamos que devuelve True
        result = my_manager.calculate_balance(iban)
        self.assertEqual(result, True)

        # ahora comprobamos que el deposit_store se ha
        # modificado con los datos correctos
        # al ser una lista, se van añadiendo al final, por lo que el
        # último componente debe coincidir con los params esperados
        # seguiremos el mismo proceso para los test válidos que deben
        # modificar el archivo balance
        balance_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        archivo_existe = os.path.exists(balance_store_test)
        if archivo_existe:
            with open(balance_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
                ultimo_registro = contenido_nuevo[-1]
                self.assertEqual(ultimo_registro["IBAN"], iban,
                                 "Exception: La transacción no se ha introducido correctamente")
                self.assertEqual(ultimo_registro["balance"], balance,
                                 "Exception: El balance no se ha calculado correctamente")
                self.assertEqual(ultimo_registro["date"], date,
                                 "Exception: La fecha no se ha calculado correctamente")

        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(balance_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test2_invalid(self):
        """ doc string del metodo"""
        #iban introducido inválido
        iban = "ES86583420445412164"

        my_manager = AccountManager()
        balance_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        if os.path.exists(balance_store_test):
            with open(balance_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = []

        # mensaje de error esperado
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.calculate_balance(iban)
        self.assertEqual(cm.exception.message, "Exception: el iban no es válido")

        # ahora comprobamos que el deposit_store no se ha modificado si esque ya existía

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test3_invalid(self):
        """ doc string del metodo"""
        # iban válido pero el archivo transactions no encontrado
        iban = "ES8658342044541216872704"

        my_manager = AccountManager()
        balance_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        transactions_path = os.path.join(os.path.dirname(__file__),
                                         "../../JsonFiles/RF3/transactions.json")
        # Guardar y eliminar temporalmente transactions
        if os.path.exists(transactions_path):
            os.rename(transactions_path, transactions_path + ".bak")

        if os.path.exists(balance_store_test):
            with open(balance_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = []

        # mensaje de error esperado
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.calculate_balance(iban)
        self.assertEqual(cm.exception.message, "Exception: archivo no encontrado")

        #despues de la prueba desbloqueamos transactions
        # Restaurar transactions
        if os.path.exists(transactions_path + ".bak"):
            os.rename(transactions_path + ".bak", transactions_path)

        # ahora comprobamos que el deposit_store no se ha modificado si esque ya existía

        deposit_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        archivo_existe = os.path.exists(deposit_store_test)
        if archivo_existe:
            with open(deposit_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:  # si el archivo no estaba y se ha creado tmb está mal
            self.assertFalse(os.path.exists(deposit_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test4_invalid(self):
        """ doc string del metodo"""
        # iban válido, pero el archivo transactions tiene un formato inválido
        iban = "ES8658342044541216872704"
        my_manager = AccountManager()
        transactions_path = os.path.join(os.path.dirname(__file__),
                                         "../../JsonFiles/RF3/transactions.json")
        balance_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        if os.path.exists(balance_store_test):
            with open(balance_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = []
            # Guardar transactions original

        if os.path.exists(transactions_path):
            with open(transactions_path, "r", encoding="utf-8") as f:
                trans_original = f.read()

        # Cambiamos el archivo transactions temporalmente
        try:
            with open(transactions_path, "w", encoding="utf-8") as f:
                f.write("ESTE NO ES UN JSON VÁLIDO {][}")

            # mensaje de error esperado
            with self.assertRaises(AccountManagementException) as cm:
                my_manager.calculate_balance(iban)
            self.assertEqual(cm.exception.message, "Exception: formato JSON inválido")
        finally:
            with open(transactions_path, "w", encoding="utf-8") as f:
                f.write(trans_original)

        # ahora comprobamos que el deposit_store no se ha modificado si esque ya existía
        if os.path.exists(balance_store_test):
            with open(balance_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                "Exception: el archivo balance_store.json ha sido modificado incorrectamente")
        else:
            self.assertFalse(os.path.exists(balance_store_test),
                             "Exception: balance_store.json no debería haberse creado")


    def test5_invalid(self):
        """ doc string del metodo"""
        #el iban es correcto pero no coincide con ningún iban de transactions
        iban = "ES9121000418450200051332"
        my_manager = AccountManager()
        balance_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        if os.path.exists(balance_store_test):
            with open(balance_store_test, "r", encoding="utf-8") as archivo:
                contenido_org = json.load(archivo)
        else:
            contenido_org = []

        #mensaje de error esperado
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.calculate_balance(iban)
        self.assertEqual(cm.exception.message, "Exception: el IBAN no se encuentra")

        # ahora comprobamos que el deposit_store no se ha modificado si esque ya existía

        balance_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        archivo_existe = os.path.exists(balance_store_test)
        if archivo_existe:
            with open(balance_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
            self.assertEqual(contenido_nuevo, contenido_org,
                             "Exception: el archivo de almacenamiento ha sido modificado")
        else:
            self.assertFalse(os.path.exists(balance_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")
    def test6_valid(self):
        """ doc string del metodo"""
        #iban es correcto y coincide con algún iban de transactions, se
        # crea balance_store por primera vez
        iban = "ES8658342044541216872704"
        my_manager = AccountManager()
        balance_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        if os.path.exists(balance_store_test):
            os.remove(balance_store_test)  # Simulamos que no existe

        transactions_file = os.path.join(os.path.dirname(__file__),
                                         "../../JsonFiles/RF3/transactions.json")
        if os.path.exists(transactions_file):
            with open(transactions_file, "r", encoding="utf-8") as archivo:
                trans_original = json.load(archivo)
        else:
            raise AccountManagementException("Exception: archivo de transacciones no encontrado")

        balance = 0
        for transaccion in trans_original:
            if transaccion["IBAN"] == iban:
                balance += float(transaccion["amount"])
        date = datetime.now().strftime("%d/%m/%Y")
        result = my_manager.calculate_balance(iban)
        self.assertEqual(result, True)

        # ahora comprobamos que el deposit_store se ha modificado con los datos correctos
        balance_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        archivo_existe = os.path.exists(balance_store_test)
        if archivo_existe:
            with open(balance_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
                ultimo_registro = contenido_nuevo[-1]
                self.assertEqual(ultimo_registro["IBAN"], iban,
                                 "Exception: La transacción no se ha introducido correctamente")
                self.assertEqual(ultimo_registro["balance"], balance,
                                 "Exception: El balance no se ha calculado correctamente")
                self.assertEqual(ultimo_registro["date"], date,
                                 "Exception: La fecha no se ha calculado correctamente")

        else:
            self.assertFalse(os.path.exists(balance_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test7_1_valid(self):
        """ doc string del metodo"""
        #iban es correcto (pero otro) y coincide con algunos de los
        # transactions, comprobamos que los resultados son los esperados
        iban = "ES6211110783482828975098"
        my_manager = AccountManager()
        transactions_file = os.path.join(os.path.dirname(__file__),
                                         "../../JsonFiles/RF3/transactions.json")
        if os.path.exists(transactions_file):
            with open(transactions_file, "r", encoding="utf-8") as archivo:
                trans_original = json.load(archivo)
        else:
            raise AccountManagementException("Exception: archivo de transacciones no encontrado")

        balance = 0
        for transaccion in trans_original:
            if transaccion["IBAN"] == iban:
                balance += float(transaccion["amount"])
        date = datetime.now().strftime("%d/%m/%Y")
        result = my_manager.calculate_balance(iban)
        self.assertEqual(result, True)

        # ahora comprobamos que el deposit_store se ha modificado con los datos correctos
        balance_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        archivo_existe = os.path.exists(balance_store_test)
        if archivo_existe:
            with open(balance_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
                ultimo_registro = contenido_nuevo[-1]
                self.assertEqual(ultimo_registro["IBAN"], iban,
                                 "Exception: La transacción no se ha introducido correctamente")
                self.assertEqual(ultimo_registro["balance"], balance,
                                 "Exception: El balance no se ha calculado correctamente")
                self.assertEqual(ultimo_registro["date"], date,
                                 "Exception: La fecha no se ha calculado correctamente")

        else:
            self.assertFalse(os.path.exists(balance_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test7_2_valid(self):
        """ doc string del metodo"""
        #iban es correcto (pero otro) y coincide con algunos de los
        # transactions, comprobamos que los resultados son los esperados
        iban = "ES3559005439021242088295"
        my_manager = AccountManager()

        transactions_file = os.path.join(os.path.dirname(__file__),
                                         "../../JsonFiles/RF3/transactions.json")
        if os.path.exists(transactions_file):
            with open(transactions_file, "r", encoding="utf-8") as archivo:
                trans_original = json.load(archivo)
        else:
            raise AccountManagementException("Exception: archivo de transacciones no encontrado")

        balance = 0
        for transaccion in trans_original:
            if transaccion["IBAN"] == iban:
                balance += float(transaccion["amount"])
        date = datetime.now().strftime("%d/%m/%Y")
        result = my_manager.calculate_balance(iban)
        self.assertEqual(result, True)

        #ahora comprobamos que el deposit_store se ha modificado con los datos correctos
        balance_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        archivo_existe = os.path.exists(balance_store_test)
        if archivo_existe:
            with open(balance_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
                ultimo_registro = contenido_nuevo[-1]
                self.assertEqual(ultimo_registro["IBAN"], iban,
                                 "Exception: La transacción no se ha introducido correctamente")
                self.assertEqual(ultimo_registro["balance"], balance,
                                 "Exception: El balance no se ha calculado correctamente")
                self.assertEqual(ultimo_registro["date"], date,
                                 "Exception: La fecha no se ha calculado correctamente")

        else:
            self.assertFalse(os.path.exists(balance_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")

    def test7_3_valid(self):
        """ doc string del metodo"""
        #iban es correcto (pero otro) y coincide con algunos de
        # los transactions, comprobamos que los resultados son los esperados
        iban = "ES7156958200176924034556"
        my_manager = AccountManager()

        transactions_file = os.path.join(os.path.dirname(__file__),
                                         "../../JsonFiles/RF3/transactions.json")
        if os.path.exists(transactions_file):
            with open(transactions_file, "r", encoding="utf-8") as archivo:
                trans_original = json.load(archivo)
        else:
            raise AccountManagementException("Exception: archivo de transacciones no encontrado")

        balance = 0
        for transaccion in trans_original:
            if transaccion["IBAN"] == iban:
                balance += float(transaccion["amount"])
        date = datetime.now().strftime("%d/%m/%Y")
        result = my_manager.calculate_balance(iban)
        self.assertEqual(result, True)

        # ahora comprobamos que el deposit_store se ha modificado con los datos correctos
        balance_store_test = os.path.join(os.path.dirname(__file__),
                                          "../../JsonFiles/RF3/balance_store.json")
        archivo_existe = os.path.exists(balance_store_test)
        if archivo_existe:
            with open(balance_store_test, "r", encoding="utf-8") as archivo:
                contenido_nuevo = json.load(archivo)
                ultimo_registro = contenido_nuevo[-1]
                self.assertEqual(ultimo_registro["IBAN"], iban,
                                 "Exception: La transacción no se ha introducido correctamente")
                self.assertEqual(ultimo_registro["balance"], balance,
                                 "Exception: El balance no se ha calculado correctamente")
                self.assertEqual(ultimo_registro["date"], date,
                                 "Exception: La fecha no se ha calculado correctamente")

        else:
            self.assertFalse(os.path.exists(balance_store_test),
                             "Exception: el archivo de almacenamiento se ha creado incorrectamente")


if __name__ == '__main__':
    unittest.main()
