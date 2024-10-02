// const grpc = require('grpc');
// const protoLoader = require('@grpc/proto-loader');
// const path = require('path');

// // Carga el archivo proto
// const PROTO_PATH = path.join(__dirname, 'stock.proto');  // Asegúrate de que esta ruta sea correcta
// const stockProto = grpc.loadPackageDefinition(protoLoader.loadSync(PROTO_PATH, { keepCase: true, longs: String, defaults: true, oneofs: true }));

// const client = new stockProto.StockearteService('localhost:50051', grpc.credentials.createInsecure());

// // Crear un usuario
// function crearUsuario(username, password, tiendaId) {
//     const request = {
//         username: username,
//         password: password,
//         tienda_id: tiendaId,
//         nombre: "Nombre Ejemplo",
//         apellido: "Apellido Ejemplo",
//         habilitado: true
//     };
    
//     client.crearUsuario(request, (error, response) => {
//         if (error) {
//             console.error('Error al crear usuario:', error);
//         } else {
//             console.log('Usuario creado:', response);
//         }
//     });
// }

// // Autenticar un usuario
// function autenticarUsuario(username, password) {
//     const request = {
//         username: username,
//         password: password
//     };
    
//     client.autenticarUsuario(request, (error, response) => {
//         if (error) {
//             console.error('Error al autenticar usuario:', error);
//         } else {
//             console.log('Usuario autenticado:', response);
//         }
//     });
// }

// // Crear una tienda
// function crearTienda(codigo, nombre, direccion, ciudad, provincia) {
//     const request = {
//         codigo: codigo,
//         nombre: nombre,
//         direccion: direccion,
//         ciudad: ciudad,
//         provincia: provincia,
//         habilitada: true,
//         casa_central: false,
//         cadena_id_cadena: 1  // Ajusta según el ID de la cadena
//     };

//     client.crearTienda(request, (error, response) => {
//         if (error) {
//             console.error('Error al crear tienda:', error);
//         } else {
//             console.log('Tienda creada:', response);
//         }
//     });
// }

// // Ejemplo de uso
// const codigoTienda = "A0ER1";  // Ejemplo de código de tienda
// crearUsuario('usuario1', 'contrasena123', 1);  // Cambia el ID de la tienda según sea necesario
// autenticarUsuario('usuario1', 'contrasena123');
// crearTienda(codigoTienda, 'Tienda Ejemplo', 'Calle Falsa 123', 'Ciudad Ejemplo', 'Provincia Ejemplo');
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const express = require('express');

// Carga del archivo .proto
const PROTO_PATH = path.join(__dirname, 'proto', 'stock.proto'); 
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});
const stock_proto = grpc.loadPackageDefinition(packageDefinition).stock;

// Creación del cliente gRPC
const client = new stock_proto.StockearteService('localhost:50051', grpc.credentials.createInsecure());

// Creación de la aplicación Express
const app = express();

// Middleware para parsear JSON
app.use(express.json());

app.use(express.static(path.join(__dirname, '..', 'frontend')));

// Ruta principal para servir el archivo login.html
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'frontend', 'login.html')); // Sirve el archivo login.html
});

// Ruta para servir el archivo index.html después de iniciar sesión
app.get('/index', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html')); // Sirve el archivo index.html
});

// Ruta para crear tienda
app.post('/crear-tienda', (req, res) => {
  const tienda = req.body;
  client.CrearTienda(tienda, (err, response) => {
    if (err) {
      console.error("Error creando tienda:", err.details);
      res.status(500).send(err.details);
      return;
    }
    res.send({ mensaje: response.mensaje });
  });
});

app.post('/crear-usuario', (req, res) => {
  const usuario = req.body;
  client.CrearUsuario(usuario, (err, response) => {
    if (err) {
      console.error("Error creando usuario:", err.details);
      res.status(500).send(err.details);
      return;
    }
    res.redirect('/login'); // Redirige al login después de crear usuario
  });
});

// Ruta para iniciar sesión
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  client.AutenticarUsuario({ nombre_usuario: username, contrasena: password }, (err, response) => {
    if (err) {
      console.error("Error iniciando sesión:", err.details);
      res.status(500).send(err.details);
      return;
    }
    if (response.exito) {
      res.redirect('/index'); // Redirige al index si el login es exitoso
    } else {
      res.status(401).send({ mensaje: response.mensaje }); // Muestra el mensaje de error si falló
    }
  });
});


const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Cliente escuchando en http://localhost:${PORT}`);
});
