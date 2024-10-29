from zeep import Client

class SoapClient:
    def __init__(self, wsdl_url):
        self.client = Client(wsdl_url)

    def obtener_datos(self):
        # Aquí llamas a tu operación SOAP
        return self.client.service.ObtenerOrdenCompra(id=1)  # Cambia el id según lo que necesites
