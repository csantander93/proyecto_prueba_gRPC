// const grpc = require('@grpc/grpc-js');
// const protoLoader = require('@grpc/proto-loader');
// const path = require('path');
// const express = require('express');

// // Carga del archivo .proto
// const PROTO_PATH = path.join(__dirname, 'proto', 'stock.proto');
// const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
//   keepCase: true,
//   longs: String,
//   enums: String,
//   defaults: true,
//   oneofs: true
// });
// const stock_proto = grpc.loadPackageDefinition(packageDefinition).stock;

// // Creación del cliente gRPC
// const client = new stock_proto.StockearteService('localhost:50051', grpc.credentials.createInsecure());



// // Creación de la aplicación Express
// const app = express();

// // Middleware para parsear JSON y servir archivos estáticos
// app.use(express.json());
// app.use(express.static(path.join(__dirname, '..', 'frontend')));

// // Funciones gRPC

// // Crear un usuario
// function crearUsuario(usuario, callback) {
//   client.CrearUsuario(usuario, callback);
// }

// // Autenticar un usuario
// function autenticarUsuario(usuario, callback) {
//   client.AutenticarUsuario(usuario, callback);
// }

// // Crear una tienda
// function crearTienda(tienda, callback) {
//   client.CrearTienda(tienda, callback);
// }

// // Crear una tienda
// function crearOrdenDeCompra(orden_compra, callback) {
//   client.CrearOrdenDeCompra(orden_compra, callback);
// }

// // Listar tiendas de casa central
// function listarTiendasCasaCentral(callback) {
//   client.ListarTiendasCasaCentral({}, callback);
// }

// // Listar todas las tiendas
// function listarTiendas(callback) {
//   client.ListarTiendas({}, callback);
// }

// // Rutas de Express

// // Ruta principal para servir el archivo login.html
// app.get('/login', (req, res) => {
//   res.sendFile(path.join(__dirname, '..', 'frontend', 'login.html')); // Sirve el archivo login.html
// });

// // Ruta para servir el archivo index.html después de iniciar sesión
// app.get('/index', (req, res) => {
//   res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html')); // Sirve el archivo index.html
// });

// // Ruta para crear usuario
// app.post('/crear-usuario', (req, res) => {
//   const usuario = req.body;
//   crearUsuario(usuario, (err, response) => {
//     if (err) {
//       console.error("Error creando usuario:", err.details);
//       res.status(500).send(err.details);
//       return;
//     }
//     res.redirect('/login'); // Redirige al login después de crear usuario
//   });
// });

// // Ruta para iniciar sesión
// app.post('/login', (req, res) => {
//   const { username, password } = req.body;
//   autenticarUsuario({ nombre_usuario: username, contrasena: password }, (err, response) => {
//     if (err) {
//       console.error("Error iniciando sesión:", err.details);
//       res.status(500).send(err.details);
//       return;
//     }
//     if (response.exito) {
//       res.redirect('/index'); // Redirige al index si el login es exitoso
//     } else {
//       res.status(401).send({ mensaje: response.mensaje }); // Muestra el mensaje de error si falló
//     }
//   });
// });


// // Ruta para crear tienda
// app.post('/crear-tienda', (req, res) => {
//   const tienda = req.body;
//   crearTienda(tienda, (err, response) => {
//     if (err) {
//       console.error("Error creando tienda:", err.details);
//       res.status(500).send(err.details);
//       return;
//     }
//     res.send({ mensaje: response.mensaje });
//   });
// });


// app.post('/orden-compra', (req, res) => {
//   const nuevaOrden = {
//       codigo_tienda: req.body.codigo_tienda,
//       items: req.body.items,
//       observaciones: req.body.observaciones
//   };

//   client.CrearOrdenDeCompra(nuevaOrden, (error, response) => {
//       if (error) {
//           console.error('Error al crear la orden:', error);
//           return res.status(500).send('Error al crear la orden de compra');
//       }
//       console.log('Respuesta gRPC:', response);
//       res.json(response);
//   });
// });




// // Ruta para obtener todas las tiendas
// app.get('/tiendas', (req, res) => {
//   listarTiendas((err, response) => {
//     if (err) {
//       console.error("Error obteniendo tiendas:", err.details);
//       res.status(500).send(err.details);
//       return;
//     }
//     res.json(response.tiendas); // Envía la lista de tiendas como respuesta
//   });
// });

// // Ruta para obtener tiendas de casa central
// app.get('/tiendas-casa-central', (req, res) => {
//   listarTiendasCasaCentral((err, response) => {
//     if (err) {
//       console.error("Error obteniendo tiendas de casa central:", err.details);
//       res.status(500).send(err.details);
//       return;
//     }
//     res.json(response.tiendas); // Envía la lista de tiendas como respuesta
//   });
// });



// // Iniciar el servidor
// const PORT = process.env.PORT || 3000;
// app.listen(PORT, () => {
//   console.log(`Cliente escuchando en http://localhost:${PORT}`);
// });

const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const express = require('express');

// Carga del archivo .proto para stock
const PROTO_PATH_STOCK = path.join(__dirname, 'proto', 'stock.proto');
const packageDefinitionStock = protoLoader.loadSync(PROTO_PATH_STOCK, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});
// Carga del archivo .proto para tienda
const PROTO_PATH_TIENDA = path.join(__dirname, 'proto', 'tienda.proto');
const packageDefinitionTienda = protoLoader.loadSync(PROTO_PATH_TIENDA, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});
const tienda_proto = grpc.loadPackageDefinition(packageDefinitionTienda).tienda;

// Creación del cliente gRPC para Stock
const stockClient = new stock_proto.StockearteService('localhost:50051', grpc.credentials.createInsecure());

// Creación del cliente gRPC para Tienda
const tiendaClient = new tienda_proto.TiendaService('localhost:50051', grpc.credentials.createInsecure());

// Creación de la aplicación Express
const app = express();

// Middleware para parsear JSON y servir archivos estáticos
app.use(express.json());
app.use(express.static(path.join(__dirname, '..', 'frontend')));

// Funciones gRPC

// Crear un usuario
function crearUsuario(usuario, callback) {
  stockClient.CrearUsuario(usuario, callback);
}

// Autenticar un usuario
function autenticarUsuario(usuario, callback) {
  stockClient.AutenticarUsuario(usuario, callback);
}

// Crear una tienda
function crearTienda(tienda, callback) {
  tiendaClient.CrearTienda(tienda, callback);
}

// Crear una orden de compra
function crearOrdenDeCompra(orden_compra, callback) {
  tiendaClient.CrearOrdenDeCompra(orden_compra, callback); // Asegúrate de que este método exista en tienda.proto
}

// Listar tiendas de casa central
function listarTiendasCasaCentral(callback) {
  tiendaClient.ListarTiendasCasaCentral({}, callback);
}

// Listar todas las tiendas
function listarTiendas(callback) {
  tiendaClient.ListarTiendas({}, callback);
}

// Rutas de Express

// Ruta principal para servir el archivo login.html
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'frontend', 'login.html')); // Sirve el archivo login.html
});

// Ruta para servir el archivo index.html después de iniciar sesión
app.get('/index', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html')); // Sirve el archivo index.html
});

// Ruta para crear usuario
app.post('/crear-usuario', (req, res) => {
  const usuario = req.body;
  crearUsuario(usuario, (err, response) => {
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
  autenticarUsuario({ nombre_usuario: username, contrasena: password }, (err, response) => {
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

// Ruta para crear tienda
app.post('/crear-tienda', (req, res) => {
  const tienda = req.body;
  crearTienda(tienda, (err, response) => {
    if (err) {
      console.error("Error creando tienda:", err.details);
      res.status(500).send(err.details);
      return;
    }
    res.send({ mensaje: response.mensaje });
  });
});



// Ruta para obtener tiendas de casa central
app.get('/tiendas-casa-central', (req, res) => {
  listarTiendasCasaCentral((err, response) => {
    if (err) {
      console.error("Error obteniendo tiendas de casa central:", err.details);
      res.status(500).send(err.details);
      return;
    }
    res.json(response.tiendas); // Envía la lista de tiendas como respuesta
  });
});

// Iniciar el servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Cliente escuchando en http://localhost:${PORT}/login`);
});
