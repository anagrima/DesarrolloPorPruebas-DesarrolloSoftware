"""class for testing the regsiter_order method"""
import hashlib
import json
import os
import unittest
from freezegun import freeze_time
from uc3m_money import AccountManager, AccountManagementException

class MyTestTransfer(unittest.TestCase):
    """class for testing the register_order method"""

    @freeze_time("22/03/2025")
    def test1_f1_valid(self):
        """ doc string del metodo"""
        #test valido
        from_iban = "ES9121000418450200051332"
        to_iban = "ES3559005439021242088295"
        concept = "Prueba superada"
        tipe = "ORDINARY"
        date = "10/04/2025"  #puedo simular que la transferencia la hago
        # antes o deespues con el freeztime
        amount = 10.00
        my_manager = AccountManager()
        file_store = os.path.join(os.path.dirname(__file__),
                                  "../../JsonFiles/RF1/transfer_store.json")
        # forzamos a que el archivo esté vacío si o si
        with open(file_store, "w", encoding="utf-8", newline="") as file:
            file.write("[]")

        result = my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                             concept=concept, tipe=tipe,
                                             date=date, amount=amount)
        #fichero = my_manager.guardar_json()
        self.assertEqual(result, "7e1f7a0e962221f10a8aac4b8a63f6b7")

        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            self.fail("fichero no existe")

        found = False
        for item in data_list:
            if item["transfer_code"] == result:
                found = True
                self.assertEqual(item["from_iban"], from_iban)
                self.assertEqual(item["to_iban"], to_iban)
                self.assertEqual(item["transfer_concept"], concept)
                self.assertEqual(item["transfer_type"], tipe)
                self.assertEqual(item["transfer_date"], date)
                self.assertEqual(float(item["transfer_amount"]), amount)

        self.assertTrue(found)

    def test2_f1_not_valid(self):
        """ doc string del metodo"""
        # from: Probar que en vez de ES sea DE
        from_iban = "DE9121000418450200051332"
        to_iban = "iban valido"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_fromNoEs.json"

        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()


        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: from_iban no es válido")

    def test3_f1_not_valid(self):
        """ doc string del metodo"""
        # from: Iban no es string
        from_iban = 912514650100971756460833
        to_iban = "iban valido"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_fromNoStr.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:

            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: from_iban no es válido")

    def test4_f1_not_valid(self):
        """ doc string del metodo"""
        # from: Iban con una longitud de 23
        from_iban = "ES912100041845020005133"
        to_iban = "iban valido"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_from23.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:

            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: from_iban no es válido")

    def test5_f1_not_valid(self):
        """ doc string del metodo"""
        # from: Iban con una longitud de 25
        from_iban = "ES91210004184502000513322"
        to_iban = "iban valido"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_from25.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:

            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: from_iban no es válido")

    def test6_f1_not_valid(self):
        """ doc string del metodo"""
        # from: Despues de ES no hay 22 números
        from_iban = "ESDHFIEMANF"
        to_iban = "iban valido"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_fromESnoNum.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: from_iban no es válido")

    def test7_f1_not_valid(self):
        """ doc string del metodo"""
        # from: Algoritmo no valido
        from_iban = "ES9121000418450200051333"
        to_iban = "iban valido"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_fromAlg.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: from_iban no es válido")

    def test8_f1_not_valid(self):
        """ doc string del metodo"""
        # to: Iban no es string
        from_iban = "ES9121000418450200051332"
        to_iban = 912514650100971756460833
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_toNoStr.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: to_iban no es válido")

    def test9_f1_not_valid(self):
        """ doc string del metodo"""
        # to: Algoritmo no valido
        from_iban = "ES9121000418450200051332"
        to_iban = "ES9121000418450200051333"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_toAlg.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: to_iban no es válido")

    def test10_f1_not_valid(self):
        """ doc string del metodo"""
        # to: Iban con una longitud de 25
        from_iban = "ES9121000418450200051332"
        to_iban = "ES91210004184502000513322"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_to25.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: to_iban no es válido")

    def test11_f1_not_valid(self):
        """ doc string del metodo"""
        # to: Iban con una longitud de 23
        from_iban = "ES9121000418450200051332"
        to_iban = "ES912100041845020005133"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_to23.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: to_iban no es válido")

    def test12_f1_not_valid(self):
        """ doc string del metodo"""
        # to: Probar que en vez de ES sea DE
        from_iban = "ES9121000418450200051332"
        to_iban = "DE9121000418450200051332"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_toNoEs.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: to_iban no es válido")

    def test13_f1_not_valid(self):
        """ doc string del metodo"""
        # to: Despues de ES no hay 22 números
        from_iban = "ES9121000418450200051332"
        to_iban = "ESDHFIEMANF"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_toESnoNum.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: to_iban no es válido")

    def test14_f1_not_valid(self):
        """ doc string del metodo"""
        # to: from_iban y to_iban son iguales
        from_iban = "ES9121000418450200051332"
        to_iban = "ES9121000418450200051332"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_toYfrom.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: from_iban y to_iban son iguales")

    def test15_f1_not_valid(self):
        """ doc string del metodo"""
        # concept: No es string
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = 112345
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_conceptNoStr.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: el concepto no tiene un valor válido")

    def test16_f1_not_valid(self):
        """ doc string del metodo"""
        # concept: solo una cadena
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "cadena"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_conceptCaden.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: el concepto no tiene un valor válido")

    def test17_f1_not_valid(self):
        """ doc string del metodo"""
        # concept: string de numeros
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "1234 45653"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_conceptCadNum.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: el concepto no tiene un valor válido")

    def test18_f1_not_valid(self):
        """ doc string del metodo"""
        # concept: dos cadenas de longitud 9
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "cadena de"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_concept9.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: el concepto no tiene un valor válido")

    def test19_f1_not_valid(self):
        """ doc string del metodo"""
        # concept: dos cadenas de longitud 31
        from_iban = "ES9121000418450200051332"
        to_iban = "ES9121000418450200051332"
        concept = "cadena de longitud mayor que 31 caracteres"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_concept31.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: el concepto no tiene un valor válido")

    def test20_f1_not_valid(self):
        """ doc string del metodo"""
        # Type: no es str
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = 1234
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_typeNoStr.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: el tipo de transferencia no es válido")

    def test21_f1_not_valid(self):
        """ doc string del metodo"""
        # Type: str no valido
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "hola"
        date = "12/04/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_typeStrNo.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: el tipo de transferencia no es válido")

    def test22_f1_not_valid(self):
        """ doc string del metodo"""
        # date: no es str
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = 12 / 11 / 2025
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_dateNoStr.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la fecha de transferencia no es válida")

    def test23_f1_not_valid(self):
        """ doc string del metodo"""
        # date: DD < 1
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "00/01/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_dateDDMenor.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la fecha de transferencia no es válida")

    def test24_f1_not_valid(self):
        """ doc string del metodo"""
        # date: DD > 31
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "32/01/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_dateDDMayor.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la fecha de transferencia no es válida")

    def test25_f1_not_valid(self):
        """ doc string del metodo"""
        # date: < fecha recibo orden
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "01/01/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_dateRecibo.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la fecha de transferencia no es válida")

    def test26_f1_not_valid(self):
        """ doc string del metodo"""
        # date: longitud 9
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "1/01/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_date9.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la fecha de transferencia no es válida")

    def test27_f1_not_valid(self):
        """ doc string del metodo"""
        # date: longitud 11
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "001/01/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_date11.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la fecha de transferencia no es válida")

    def test28_f1_not_valid(self):
        """ doc string del metodo"""
        # date: no valida
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "31/02/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_dateNoValida.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la fecha de transferencia no es válida")

    def test29_f1_not_valid(self):
        """ doc string del metodo"""
        # amount: no es float
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 1
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_amountNoFloat.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

    def test30_f1_not_valid(self):
        """ doc string del metodo"""
        # amount: < 10,00
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 9.99
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_amount10.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

    def test31_f1_not_valid(self):
        """ doc string del metodo"""
        # amount: > 10000,00
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 10000.01
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_amount10000.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

    def test32_f1_not_valid(self):
        """ doc string del metodo"""
        # amount: tres decimales
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "12/04/2025"
        amount = 9.999
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_amountDeci.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la cantidad no es válida")

    def test34_f1_not_valid(self):
        """ doc string del metodo"""
        # date: MM < 01
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "01/00/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_dateMMMenor.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la fecha de transferencia no es válida")

    def test35_f1_not_valid(self):
        """ doc string del metodo"""
        # date: MM > 12
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "01/13/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_dateMMMayor.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la fecha de transferencia no es válida")

    def test36_f1_not_valid(self):
        """ doc string del metodo"""
        # date: YY < 2025
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "01/01/2024"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_dateYYMenor.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la fecha de transferencia no es válida")

    def test37_f1_not_valid(self):
        """ doc string del metodo"""
        # date: YY > 2050
        from_iban = "ES9121000418450200051332"
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "INMEDIATE"
        date = "01/01/2051"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_dateYYMayor.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: la fecha de "
                                               "transferencia no es válida")

#pruebas adicionales
    # aunque ya hayamos probado que la función funciona
    # correctamente para un caso válido, generamos más para otros casos
    @freeze_time("22/12/2024")
    def test38_valid_transfer(self):
        """Valid transfer con amount siendo un valor límite"""
        from_iban = "ES9121000418450200051332"
        to_iban = "ES3559005439021242088295"
        concept = "Sol brilla hoy"
        tipe = "URGENT"
        date = "02/02/2026"
        amount = 10.01
        my_manager = AccountManager()
        file_store = os.path.join(os.path.dirname(__file__),
                                  "../../JsonFiles/RF1/transfer_store.json")

        result = my_manager.transfer_request(from_iban, to_iban, concept, tipe, date, amount)

        with open(file_store, "r", encoding="utf-8") as file:
            data_list = json.load(file)

        self.assertTrue(any(t["transfer_code"] == result for t in data_list))

        self.assertEqual(result, "2a6a1069ddbf911b0fef4a84f682e54d")
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            self.fail("fichero no existe")

        found = False
        for item in data_list:
            if item["transfer_code"] == result:
                found = True
                self.assertEqual(item["from_iban"], from_iban)
                self.assertEqual(item["to_iban"], to_iban)
                self.assertEqual(item["transfer_concept"], concept)
                self.assertEqual(item["transfer_type"], tipe)
                self.assertEqual(item["transfer_date"], date)
                self.assertEqual(float(item["transfer_amount"]), amount)

        self.assertTrue(found)

    @freeze_time("22/03/2025")
    def test39_valid_transfer(self):
        """ doc string del metodo"""
        from_iban = "ES9121000418450200051332"
        to_iban = "ES3559005439021242088295"
        concept = "La prueba fue un gran desafio"
        tipe = "INMEDIATE"
        date = "31/12/2050"  # puedo simular que la transferencia la hago
        # antes o deespues con el freeztime
        amount = 10000.00
        my_manager = AccountManager()
        file_store = os.path.join(os.path.dirname(__file__),
                                  "../../JsonFiles/RF1/transfer_store.json")

        result = my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                             concept=concept, tipe=tipe,
                                             date=date, amount=amount)
        # fichero = my_manager.guardar_json()
        self.assertEqual(result, "86a1eb1f0f40ff0920ad467ef39cfbae")

        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            self.fail("fichero no existe")

        found = False
        for item in data_list:
            if item["transfer_code"] == result:
                found = True
                self.assertEqual(item["from_iban"], from_iban)
                self.assertEqual(item["to_iban"], to_iban)
                self.assertEqual(item["transfer_concept"], concept)
                self.assertEqual(item["transfer_type"], tipe)
                self.assertEqual(item["transfer_date"], date)
                self.assertEqual(float(item["transfer_amount"]), amount)

        self.assertTrue(found)

    @freeze_time("22/12/2024")
    def test40_valid_transfer(self):
        """Valid transfer con amount siendo un valor límite"""
        from_iban = "ES9121000418450200051332"
        to_iban = "ES3559005439021242088295"
        concept = "Cuarta transferenciaconcaracts"
        tipe = "INMEDIATE"
        date = "30/11/2049"
        amount = 9999.99
        my_manager = AccountManager()
        file_store = os.path.join(os.path.dirname(__file__),
                                  "../../JsonFiles/RF1/transfer_store.json")

        result = my_manager.transfer_request(from_iban, to_iban, concept, tipe, date, amount)

        with open(file_store, "r", encoding="utf-8") as file:
            data_list = json.load(file)

        self.assertTrue(any(t["transfer_code"] == result for t in data_list))
        self.assertEqual(result, "c79fb6cf2ff243b1c4cbfe5a94193dbc")

        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            self.fail("fichero no existe")

        found = False
        for item in data_list:
            if item["transfer_code"] == result:
                found = True
                self.assertEqual(item["from_iban"], from_iban)
                self.assertEqual(item["to_iban"], to_iban)
                self.assertEqual(item["transfer_concept"], concept)
                self.assertEqual(item["transfer_type"], tipe)
                self.assertEqual(item["transfer_date"], date)
                self.assertEqual(float(item["transfer_amount"]), amount)

        self.assertTrue(found)

    def test41_not_valid(self):
        """ doc string del metodo"""
        #una prueba más de iban no válido
        from_iban = ""
        to_iban = "ES8658342044541216872704"
        concept = "esto es una prueba"
        tipe = "URGENT"
        date = "01/00/2025"
        amount = 250.14
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_In_from.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                                 concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message, "Exception: from_iban no es válido")


    @freeze_time("22/12/2024")
    def test42_valid_transfer(self):
        """Valid transfer con amount siendo otro valor límite"""
        from_iban = "ES9121000418450200051332"
        to_iban = "ES3559005439021242088295"
        concept = "Cuarta transferenciaconcaracts"
        tipe = "INMEDIATE"
        date = "30/11/2049"
        amount = 10.5
        my_manager = AccountManager()
        file_store = os.path.join(os.path.dirname(__file__),
                                  "../../JsonFiles/RF1/transfer_store.json")

        result = my_manager.transfer_request(from_iban, to_iban, concept, tipe, date, amount)

        with open(file_store, "r", encoding="utf-8") as file:
            data_list = json.load(file)

        self.assertTrue(any(t["transfer_code"] == result for t in data_list))
        self.assertEqual(result, "dd069bc15bcf0e5598d431c8a92754e5")

        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            self.fail("fichero no existe")

        found = False
        for item in data_list:
            if item["transfer_code"] == result:
                found = True
                self.assertEqual(item["from_iban"], from_iban)
                self.assertEqual(item["to_iban"], to_iban)
                self.assertEqual(item["transfer_concept"], concept)
                self.assertEqual(item["transfer_type"], tipe)
                self.assertEqual(item["transfer_date"], date)
                self.assertEqual(float(item["transfer_amount"]), amount)

        self.assertTrue(found)

    def test43_invalid_json_format(self):
        """test para un formato no valido de transfer_store"""
        #modificamos el archivo store y luego volvemos a insertar los datos originales
        file_store = os.path.join(os.path.dirname(__file__),
                                  "../../JsonFiles/RF1/transfer_store.json")
        from_iban = "ES9121000418450200051332"
        to_iban = "ES3559005439021242088295"
        concept = "Esto es una prueba"
        tipe = "ORDINARY"
        date = "10/04/2025"
        amount = 100.00

        if os.path.exists(file_store):
            with open(file_store, "r", encoding="utf-8") as archivo:
                contenido_org = archivo.read()
        else:
            contenido_org = []
            # Guardar transactions original

        try:
            with open(file_store, "w", encoding="utf-8") as file:
                file.write("INVALID JSON")

            my_manager = AccountManager()
            with self.assertRaises(AccountManagementException) as cm:
                my_manager.transfer_request(from_iban, to_iban, concept, tipe, date, amount)

            self.assertEqual(str(cm.exception), "Exception: formato JSON inválido")
        finally:
            #devolvemos el archivo con su contenido original despues de la prueba
            with open(file_store, "w", encoding="utf-8") as file:
                file.write(contenido_org)

    @freeze_time("25/03/2025")
    def test44_f1_not_valid(self):
        """ doc string del metodo"""
        # comprobamos mensaje de error si la transacción en el fichero es ya existente
        from_iban = "ES9121000418450200051332"
        to_iban = "ES3559005439021242088295"
        concept = "Prueba superada"
        tipe = "ORDINARY"
        date = "10/04/2025"  # puedo simular que la transferencia la hago
        amount = 10.00
        my_manager = AccountManager()

        # Crear el hash y pasarle esta info al hash
        json_file_store = os.path.join(os.path.dirname(__file__), "../../JsonFiles/RF1/")
        file_store = json_file_store + "test_fichero.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file_original:
            hashlib.md5(str(file_original).encode()).hexdigest()

        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(from_iban=from_iban, to_iban=to_iban,
                                        concept=concept, tipe=tipe,
                                        date=date, amount=amount)
        self.assertEqual(cm.exception.message,
                         "Exception: existe en el archivo de "
                         "salida una transferencia con los mismos datos")

#test adicionales para la comrpobación de algunas de las funciones auxiliares y sus valores límites
    def test_validacion_amount(self):
        """Tests para valores límite en amount"""
        manager = AccountManager()

        # Exactamente 10.00 (mínimo)
        self.assertTrue(manager.validate_amount(10.00))

        # Exactamente 10000.00 (máximo)
        self.assertTrue(manager.validate_amount(10000.00))

        # 9.99 (debajo del mínimo)
        self.assertFalse(manager.validate_amount(9.99))

        # 10000.01 (encima del máximo)
        self.assertFalse(manager.validate_amount(10000.01))

        # 3 decimales (inválido)
        self.assertFalse(manager.validate_amount(10.001))

    def test_validacion_iban(self):
        """Tests detallados para validate_iban"""
        manager = AccountManager()

        # IBAN con espacios y guiones
        self.assertTrue(manager.validate_iban("ES91 2100-0418 4502 0005 1332"))

        # IBAN con minúsculas
        self.assertTrue(manager.validate_iban("es9121000418450200051332"))

        # IBAN inválido (checksum incorrecto)
        self.assertFalse(manager.validate_iban("ES9121000418450200051333"))

    def test_validacion_concept(self):
        """Tests para casos especiales de validate_concept"""
        manager = AccountManager()

        # Exactamente 10 caracteres (mínimo)
        self.assertTrue(manager.validate_concept("a b c d e "))

        # Exactamente 30 caracteres (máximo)
        self.assertTrue(manager.validate_concept("Este es un concepto de exactam"))

        # 9 caracteres (inválido)
        self.assertFalse(manager.validate_concept("a b c d"))

        # 31 caracteres (inválido)
        self.assertFalse(manager.validate_concept("Este concepto tiene más de treinta caracteres"))

        # Caracteres especiales (inválido)
        self.assertFalse(manager.validate_concept("Pago $100"))


if __name__ == '__main__':
    unittest.main()
