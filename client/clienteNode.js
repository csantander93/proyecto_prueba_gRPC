const grpc = require('grpc');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Carga el archivo proto
const PROTO_PATH = path.join(__dirname, '.proto/stock.proto');  
const stockProto = grpc.loadPackageDefinition(protoLoader.loadSync(PROTO_PATH, { keepCase: true, longs: String, defaults: true, oneofs: true }));

const client = new stockProto.StockearteService('localhost:50051', grpc.credentials.createInsecure());

// Crear un usuario
function crearUsuario(username, password, tiendaId) {
    const request = {
        username: username,
        password: password,
        tienda_id: tiendaId,
        nombre: "Nombre Ejemplo",
        apellido: "Apellido Ejemplo",
        habilitado: true
    };
    
    client.crearUsuario(request, (error, response) => {
        if (error) {
            console.error('Error al crear usuario:', error);
        } else {
            console.log('Usuario creado:', response);
        }
    });
}

// Autenticar un usuario
function autenticarUsuario(username, password) {
    const request = {
        username: username,
        password: password
    };
    
    client.autenticarUsuario(request, (error, response) => {
        if (error) {
            console.error('Error al autenticar usuario:', error);
        } else {
            console.log('Usuario autenticado:', response);
        }
    });
}

// Crear una tienda
function crearTienda(codigo, nombre, direccion, ciudad, provincia) {
    const request = {
        codigo: codigo,
        nombre: nombre,
        direccion: direccion,
        ciudad: ciudad,
        provincia: provincia,
        habilitada: true,
        casa_central: false,
        cadena_id_cadena: 1  // Ajusta según el ID de la cadena
    };

    client.crearTienda(request, (error, response) => {
        if (error) {
            console.error('Error al crear tienda:', error);
        } else {
            console.log('Tienda creada:', response);
        }
    });
}

// Ejemplo de uso
const codigoTienda = "A0ER1";  // Ejemplo de código de tienda
crearUsuario('usuario1', 'contrasena123', 1);  // Cambia el ID de la tienda según sea necesario
autenticarUsuario('usuario1', 'contrasena123');
crearTienda(codigoTienda, 'Tienda Ejemplo', 'Calle Falsa 123', 'Ciudad Ejemplo', 'Provincia Ejemplo');
