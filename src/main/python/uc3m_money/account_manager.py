"""Module """
import json
import os
from json import JSONDecodeError
from datetime import datetime

from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.transfer_request import TransferRequest


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban):
        """ doc string del metodo"""
        if not isinstance(iban, str):
            return False

        # Eliminar espacios y convertir a mayuscula
        iban = iban.strip().upper()
        iban = iban.replace(" ", "").replace("-", "")

        # Verificar que el IBAN tiene 24 caracteres
        if len(iban) != 24:
            return False

        # Verificar que los dos primeros caracteres son "ES"
        if iban[:2] != 'ES':
            return False

        # Mover los 4 primeros caracteres al final
        iban_reordenado = iban[4:] + iban[:4]

        # Convertir las letras a números (A=10, B=11, ..., Z=35)
        iban_numerico = ''
        for caracter in iban_reordenado:
            if caracter.isalpha():
                iban_numerico += str(ord(caracter) - ord('A') + 10)
            else:
                iban_numerico += caracter

        # Calcular el módulo 97 del número resultante
        resto = int(iban_numerico) % 97

        # Si el resto es 1, el IBAN es válido
        return resto == 1

    #validacion de la cantidad a transferir, AM-FR-01-I6
    @staticmethod
    def validate_amount(amount:float):
        """ doc string del metodo"""
        #verificamos que la cantidad se encuentre entre los valores definidos
        if amount < 10.00 or amount > 10000.00:
            return False
        #verificamos que maximo tiene dos decimales, para ello lo pasamos a str
        amount_str = str(amount)
        # Verificar que tiene exactamente 2 decimales
        if "." in amount_str:
            parte_decimal = amount_str.split(".")[1] #extraemos la parte decimal
            # Verificar que no tenga más de 2 decimales
            if len(parte_decimal) > 2:
                return False
        else: #si no hay punto es una cantidad entera sin decimales (válido)
            pass
        return True

    @staticmethod
    def validate_concept(concept:str):
        """ doc string del metodo"""
        if not isinstance(concept, str):
            return False
        if not "A"<=concept<="Z" and not "a"<=concept<="z":
            return False
        if len(concept) < 10 or len(concept) > 30:
            return False
        if len(concept.split()) < 2:
            return False
        return True

    @staticmethod
    def validate_type(tipe:str):
        """ doc string del metodo"""
        valid_types = {'ORDINARY', 'URGENT', 'INMEDIATE'}
        return tipe in valid_types

    @staticmethod
    def validate_date(date:str):
        """ doc string del metodo"""
        if not isinstance(date, str):
            return False

        try:
            fecha = datetime.strptime(date, "%d/%m/%Y")
            if fecha.year < 2025 or fecha.year > 2050:
                return False
            if fecha < datetime.now():
                return False
        except ValueError:
            return False
        return True

    def transfer_request(self, from_iban, to_iban, concept, tipe, date, amount):
        """ doc string del metodo"""
        if not self.validate_iban(from_iban):
            raise AccountManagementException("Exception: from_iban no es válido")
        if not self.validate_iban(to_iban):
            raise AccountManagementException("Exception: to_iban no es válido")
        if not self.validate_amount(amount):
            raise AccountManagementException("Exception: la cantidad no es válida")
        if not self.validate_concept(concept):
            raise AccountManagementException("Exception: el concepto no tiene un valor válido")
        if not self.validate_date(date):
            raise AccountManagementException("Exception: la fecha de transferencia no es válida")
        if not self.validate_type(tipe):
            raise AccountManagementException("Exception: el tipo de transferencia no es válido")

        if from_iban == to_iban:
            raise AccountManagementException("Exception: from_iban y to_iban son iguales")

        my_transfer = TransferRequest(from_iban=from_iban, to_iban=to_iban,
                                      transfer_concept= concept, transfer_type= tipe,
                                      transfer_date = date, transfer_amount = amount)

        #leer el fichero
        json_file_store = os.path.join(os.path.dirname(__file__), "../../../JsonFiles/RF1/")
        file_store = json_file_store + "transfer_store.json"

        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("Exception: formato JSON inválido") from ex
        #comprobar si esa transferencia ya existe en el transfer_store, donde
        # almacenamos las transferencias
        transfer_data = my_transfer.to_json()
        for transferencia in data_list:
            if all(
                    transferencia[key] == transfer_data[key]
                    for key in ["from_iban", "to_iban", "transfer_type",
                                "transfer_concept", "transfer_date"]
            ) and float(transferencia["transfer_amount"]) == amount:
                raise AccountManagementException(
                    "Exception: existe en el archivo de "
                    "salida una transferencia con los mismos datos"
                )
        data_list.append(my_transfer.to_json())
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except Exception as ex:
            raise AccountManagementException("Exception: error al escribir en el archivo") from ex

        return my_transfer.transfer_code

    def deposit_into_acount(self, input_file:str):
        """ doc string del metodo"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                deposit_list = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Exception: no hay fichero de entrada") from ex
        except JSONDecodeError as ex:
            raise AccountManagementException("Exception: formato JSON inválido") from ex

        try:
            iban = deposit_list["IBAN"]
        except KeyError as ex:
            raise AccountManagementException("Exception: nombre clave IBAN incorrecta") from ex
        try:
            amount = deposit_list["AMOUNT"]
        except KeyError as ex:
            raise AccountManagementException("Exception: nombre clave AMOUNT incorrecta") from ex

        if not amount.startswith("EUR "):
            raise AccountManagementException("Exception: la cantidad no es válida")
        #extraemos los números de amount para verificar que cumplen con los requisitos
        num_amount = amount[4:]
        try:
            cantidad = float(num_amount)
        except ValueError as ex:
            raise AccountManagementException("Exception: la cantidad no es válida") from ex
        if not self.validate_iban(iban):
            raise AccountManagementException("Exception: el iban no es válido")
        if not self.validate_amount(cantidad):
            raise AccountManagementException("Exception: la cantidad no es válida")

        my_deposit = AccountDeposit(to_iban=iban, deposit_amount=amount)

        #guardar en archivo json
        deposit_store = os.path.join(os.path.dirname(__file__),
                                     "../../../JsonFiles/RF2/deposit_store.json")
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(deposit_store), exist_ok=True)

        try:
            with open(deposit_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)

        except FileNotFoundError:
            data_list = []
        except JSONDecodeError as ex:
            raise AccountManagementException("Exception: formato JSON inválido") from ex

        for deposit in data_list:
            if deposit["to_iban"] == iban and deposit["deposit_amount"] == cantidad:
                raise AccountManagementException("Exception: existe en"
                                                 "el archivo de salida una"
                                                 "transferencia con los mismos datos")

        data_list.append(my_deposit.to_json())

        try:
            with open(deposit_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)

        except Exception as ex:
            raise AccountManagementException("Exception: error al"
                                             "escribir en el archivo") from ex

        return my_deposit.deposit_signature

    def calculate_balance(self,iban_number):
        """ doc string del metodo"""

        if not self.validate_iban(iban_number):
            raise AccountManagementException("Exception: el iban no es válido")
        # leer el fichero
        file_store = os.path.join(os.path.dirname(__file__),
                                  "../../../JsonFiles/RF3/transactions.json")
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Exception: archivo no encontrado") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("Exception: formato JSON inválido") from ex

        #primero comprobamos si el IBAN está o no en tranasactions.json
        found = False
        balance = 0
        for transferencia in data_list:
            if transferencia["IBAN"] == iban_number:
                balance += float(transferencia["amount"])
                found = True
        if not found:
            raise AccountManagementException("Exception: el IBAN no se encuentra")

        # Ruta del archivo balance_store.json
        balance_store = os.path.join(os.path.dirname(__file__),
                                     "../../../JsonFiles/RF3/balance_store.json")
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(balance_store), exist_ok=True)
        saldo = {"IBAN": iban_number, "balance": balance,
                 "date": datetime.now().strftime("%d/%m/%Y")}

        try:
            with open(balance_store, "r", encoding="utf-8", newline="") as file:
                store_antiguo = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            store_antiguo = []  # Si hay un error, inicializar como lista vacía

        store_antiguo.append(saldo)
        try:
            with open(balance_store, "w", encoding="utf-8") as file:
                json.dump(store_antiguo, file, indent=2)

        except Exception as ex:
            raise AccountManagementException("Exception: error al"
                                             "escribir en el archivo") from ex

        return True
