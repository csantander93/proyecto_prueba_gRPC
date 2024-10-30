const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const express = require('express');
const app = express();

// Ruta hacia el archivo .proto de la tienda
const STORE_PROTO_PATH = path.join(__dirname, 'proto', 'tienda.proto');
// Ruta hacia el archivo .proto de usuario
const USER_PROTO_PATH = path.join(__dirname, 'proto', 'usuario.proto');
// Ruta hacia el archivo .proto de producto
const PRODUCTO_PROTO_PATH = path.join(__dirname, 'proto', 'producto.proto');

// Cargar el tienda .proto
const packageDefinition = protoLoader.loadSync(STORE_PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

// Cargar el archivo .proto de usuario
const userPackageDefinition = protoLoader.loadSync(USER_PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

// Cargar el archivo .proto de producto
const productoPackageDefinition = protoLoader.loadSync(PRODUCTO_PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

// Obtener el paquete gRPC del archivo .proto
const tiendaProto = grpc.loadPackageDefinition(packageDefinition).tienda;
const userProto = grpc.loadPackageDefinition(userPackageDefinition).usuario;
const productoProto = grpc.loadPackageDefinition(productoPackageDefinition).producto;


// Crear un cliente para TiendaService
const tiendaClient = new tiendaProto.TiendaService('localhost:50051', grpc.credentials.createInsecure());
// Crear un cliente para UserService
const userClient = new userProto.UsuarioService('localhost:50051', grpc.credentials.createInsecure());
// Crear un cliente para ProductoService
const productoClient = new productoProto.ProductoService('localhost:50051', grpc.credentials.createInsecure());

console.log('Iniciando el cliente...');

// Middleware para parsear JSON y servir archivos estáticos
app.use(express.json());
app.use(express.static(path.join(__dirname, '..', 'frontend')));

//Funciones gRPC

function crearTienda(tienda, callback) {
  client.CrearTienda(tienda, callback);
}

function modificarTienda(tienda, callback) {
  client.ModificarTienda(tienda, callback);
}

// Crear un usuario
function crearUsuario(usuario, callback) {
  client.CrearUsuario(usuario, callback);
}

// Autenticar un usuario
function autenticarUsuario(usuario, callback) {
  client.AutenticarUsuario(usuario, callback);
}

// Crear producto
function crearProducto(tienda, callback) {
  client.CrearProducto(tienda, callback);
}

// Ruta principal para servir el archivo login.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '.', 'frontend', 'login.html'));
});

// Ruta para servir el archivo index.html después de iniciar sesión
app.get('/index', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html'));
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

// Ruta para crear una tienda
app.post('/crearTienda', (req, res) => {
  const tienda = req.body;
  console.log('Datos recibidos del formulario:', tienda);

  // Validar los datos de la tienda antes de enviarlos al servidor gRPC
  if (!tienda.codigo || !tienda.nombre || !tienda.direccion || !tienda.ciudad || !tienda.provincia || typeof tienda.habilitada !== 'boolean' || typeof tienda.casa_central !== 'boolean') {
    return res.status(400).send('Datos de tienda inválidos');
  }

  tiendaClient.CrearTienda(tienda, (err, response) => {
    if (err) {
      console.error("Error creando tienda:", err.details);
      res.status(500).json({ mensaje: err.details });
      return;
    }
    console.log('Respuesta del servidor gRPC:', response);
    res.status(201).json(response.tienda);
  });
});

// Ruta para modificar una tienda
app.put('/modificarTienda/:id', (req, res) => {
  const idTienda = req.params.id;
  const tiendaModificada = req.body;
  tiendaModificada.id_tienda = idTienda;

  console.log('Datos recibidos del formulario para modificar:', tiendaModificada);

  // Validar los datos de la tienda antes de enviarlos al servidor gRPC
  if (!tiendaModificada.codigo || !tiendaModificada.nombre || !tiendaModificada.direccion || !tiendaModificada.ciudad || !tiendaModificada.provincia || typeof tiendaModificada.habilitada !== 'boolean' || typeof tiendaModificada.casa_central !== 'boolean') {
    return res.status(400).send('Datos de tienda inválidos');
  }

  tiendaClient.ModificarTienda(tiendaModificada, (err, response) => {
    if (err) {
      console.error("Error modificando tienda:", err.details);
      res.status(500).json({ mensaje: err.details });
      return;
    }
    console.log('Respuesta del servidor gRPC:', response);
    res.status(200).json(response.tienda);
  });
});

// Ruta para borrar una tienda
app.delete('/borrarTienda/:id', (req, res) => {
  const idTienda = req.params.id;

  tiendaClient.BorrarTienda({ id_tienda: idTienda }, (error, response) => {
    if (error) {
      console.error('Error borrando tienda:', error.message);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.NOT_FOUND) {
        return res.status(404).send('Tienda no encontrada');
      } else if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error borrando tienda');
      }
    } else {
      res.status(200).send('Tienda borrada con éxito');
    }
  });
});


// Ruta para buscar una tienda
app.get('/buscarTienda/:id', (req, res) => {
  const idTienda = req.params.id;

  tiendaClient.BuscarTienda({ id_tienda: idTienda }, (error, response) => {
    if (error) {
      console.error('Error buscando tienda:', error.message);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.NOT_FOUND) {
        return res.status(404).send('Tienda no encontrada');
      } else if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error buscando tienda');
      }
    } else {
      res.status(200).json(response.tienda);
    }
  });
});

// Ruta para obtener la lista de usuarios
app.get('/obtenerUsuarios', (req, res) => {
  userClient.ObtenerUsuarios({}, (err, response) => {
    if (err) {
      console.error("Error obteniendo usuarios:", err.details);
      res.status(500).json({ mensaje: err.details });
      return;
    }
    res.status(200).json(response.usuarios);
  });
});

// Ruta para enlistar tiendas
app.get('/enlistarTiendas', (req, res) => {
  tiendaClient.EnlistarTiendas({}, (error, response) => {
    if (error) {
      console.error('Error al enlistar tiendas:', error.message);
      res.status(500).send('Error al enlistar tiendas');
    } else {
      res.status(200).json(response.tiendas);
    }
  });
});
// Función para probar EnlistarTiendas
function enlistarTiendas() {
  tiendaClient.EnlistarTiendas({}, (error, response) => {
    if (error) {
      console.error('Error enlistando tiendas:', error);
    } else {
      console.log('Tiendas encontradas:', response);
    }
  });
}

// Ruta para buscar una tienda por nombre
app.get('/buscarTiendaPorNombre/:nombre', (req, res) => {
  const nombreTienda = req.params.nombre;

  tiendaClient.BuscarTiendaPorNombre({ nombre: nombreTienda }, (error, response) => {
    if (error) {
      console.error('Error buscando tienda por nombre:', error.message);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.NOT_FOUND) {
        return res.status(404).send('Tienda no encontrada');
      } else if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error buscando tienda por nombre');
      }
    } else {
      res.status(200).json(response);
    }
  });
});
// Función para probar BuscarTiendaPorNombre
function buscarTiendaPorNombre(nombreTienda) {
  tiendaClient.BuscarTiendaPorNombre({ nombre: nombreTienda }, (error, response) => {
      if (error) {
          console.error('Error buscando tienda por nombre:', error);
      } else {
          console.log('Respuesta del servidor:', response);
      }
  });
}

// Ruta para crear un usuario
app.post('/crearUsuario', (req, res) => {
  const nuevoUsuario = req.body;

  // IMPORTANTE: Validar los datos del usuario antes de enviarlos al servidor gRPC
  if (!nuevoUsuario.username || !nuevoUsuario.password || typeof nuevoUsuario.habilitado !== 'boolean' || !nuevoUsuario.tienda_idtienda) {
    return res.status(400).send('Datos de usuario inválidos');
  }

  userClient.crearUsuario(nuevoUsuario, (error, response) => {
    if (error) {
      console.error('Error creando usuario:', error.message);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.ALREADY_EXISTS) {
        return res.status(409).send('El usuario ya existe');
      } else if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error creando usuario');
      }
    } else {
      res.status(201).json(response.usuario);
    }
  });
});
// Función para probar CrearUsuario
function crearUsuario() {
  const nuevoUsuario = {
    username: 'usuarioTest',
    password: 'passwordSeguro',
    habilitado: true,
    tienda_idtienda: 1
  };

  userClient.crearUsuario(nuevoUsuario, (error, response) => {
    if (error) {
      console.error('Error creando usuario:', error.message);
    } else {
      console.log('Usuario creado con éxito:', response.usuario);
    }
  });
}

// Ruta para modificar un usuario
app.put('/modificarUsuario/:id', (req, res) => {
  const idUsuario = req.params.id;
  const usuarioModificado = req.body;
  usuarioModificado.id_usuario = idUsuario;

  userClient.ModificarUsuario(usuarioModificado, (error, response) => {
    if (error) {
      console.error('Error modificando usuario:', error.message);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.NOT_FOUND) {
        return res.status(404).send('Usuario no encontrado');
      } else if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error modificando usuario');
      }
    } else {
      res.status(200).json(response.usuario);
    }
  });
});
// Función para probar ModificarUsuario
function modificarUsuario(idUsuario) {
  const usuarioModificado = {
    id_usuario: idUsuario,
    username: 'usuarioModificado',
    password: 'nuevoPasswordSeguro',
    habilitado: true,
    tienda_idtienda: 1
  };

  userClient.ModificarUsuario(usuarioModificado, (error, response) => {
    if (error) {
      console.error('Error modificando usuario:', error);
    } else {
      console.log('Usuario modificado con éxito:', response.usuario);
    }
  });
}

// Ruta para borrar un usuario
app.delete('/borrarUsuario/:id', (req, res) => {
  const idUsuario = req.params.id;

  userClient.borrarUsuario({ id_usuario: idUsuario }, (error, response) => {
    if (error) {
      console.error('Error borrando usuario:', error.message);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.NOT_FOUND) {
        return res.status(404).send('Usuario no encontrado');
      } else if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error borrando usuario');
      }
    } else {
      res.status(200).send('Usuario borrado con éxito');
    }
  });
});
// Función para probar BorrarUsuario
function borrarUsuario(idUsuario) {
  userClient.BorrarUsuario({ id_usuario: idUsuario }, (error, response) => {
    if (error) {
      console.error('Error borrando usuario:', error);
    } else {
      console.log('Usuario borrado con éxito:', response.usuario);
    }
  });
}

// Ruta para buscar un usuario por username
app.get('/buscarUsuario/:username', (req, res) => {
  const username = req.params.username;

  userClient.BuscarUsuario({ username: username }, (error, response) => {
    if (error) {
      console.error('Error buscando usuario:', error.details);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.NOT_FOUND) {
        return res.status(404).send('Usuario no encontrado');
      } else if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error buscando usuario');
      }
    } else if (response.usuario) {
      res.status(200).json(response.usuario);
    } else {
      res.status(404).send('Usuario no encontrado');
    }
  });
});
// Función para probar buscarUsuario
function buscarUsuario(username) {
  console.log('Buscando usuario con username:', username);
  userClient.BuscarUsuario({ username: username }, (error, response) => {
    if (error) {
      console.error('Error buscando usuario:', error.details); // Detalles del error
    } else if (response.usuario) {
      console.log('Usuario encontrado:', response.usuario);
    } else {
      console.log('Usuario no encontrado');
    }
  });
}

// Ruta para enlistar usuarios
app.get('/enlistarUsuarios', (req, res) => {
  userClient.EnlistarUsuarios({}, (error, response) => {
    if (error) {
      console.error('Error al enlistar usuarios:', error.details);
      res.status(500).send('Error al enlistar usuarios');
    } else {
      res.status(200).json(response.usuarios);
    }
  });
});
// Función para probar EnlistarUsuarios
function enlistarUsuarios() {
  userClient.EnlistarUsuarios({}, (error, response) => {
      if (error) {
          console.error('Error al enlistar usuarios:', error.details); // Muestra el error si lo hay
      } else {
          console.log('Usuarios enlistados:', response.usuarios);
          response.usuarios.forEach(usuario => {
              console.log(`ID: ${usuario.id_usuario}, Username: ${usuario.username}`);
          });
      }
  });
}

// Ruta para autenticar un usuario
app.post('/autenticarUsuario', (req, res) => {
  const { username, password } = req.body;

  // Validar los datos del usuario antes de enviarlos al servidor gRPC
  if (!username || !password) {
    return res.status(400).send('Datos de usuario inválidos');
  }

  userClient.autenticarUsuario({ username, password }, (error, response) => {
    if (error) {
      console.error('Error autenticando usuario:', error.message);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.UNAUTHENTICATED) {
        return res.status(401).send('Credenciales inválidas');
      } else if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error autenticando usuario');
      }
    } else {
      res.status(200).json(response);
    }
  });
});
// Función para probar AutenticarUsuario
function autenticarUsuario() {
  const credenciales = {
    username: 'usuarioTest2',
    password: 'passwordSeguro2'
  };

  userClient.AutenticarUsuario(credenciales, (error, response) => {
    if (error) {
      console.error('Error autenticando usuario:', error);
    } else {
      if (response.autenticado) {
        console.log('Autenticación exitosa:', response.mensaje);
      } else {
        console.log('Fallo en la autenticación:', response.mensaje);
      }
    }
  });
}

// Ruta para crear un producto
app.post('/crearProducto', (req, res) => {
  const producto = req.body;
  console.log('Datos recibidos del formulario:', producto);

  // Validar los datos del producto antes de enviarlos al servidor gRPC
  if (!producto.codigo || !producto.nombre || !producto.talle || typeof producto.color || typeof producto.stock !== 'number') {
    return res.status(400).send('Datos de producto inválidos');
  }

  productoClient.CrearProducto(producto, (err, response) => {
    if (err) {
      console.error("Error creando producto:", err.details);
      res.status(500).json({ mensaje: err.details });
      return;
    }
    console.log('Respuesta del servidor gRPC:', response);
    res.status(201).json(response.producto);
  });
});

// Ruta para modificar un producto
app.put('/modificarProducto/:id', (req, res) => {
  const idProducto = req.params.id;
  const productoModificado = req.body;
  productoModificado.id_producto = idProducto;

  // Validar los datos del producto antes de enviarlos al servidor gRPC
  if (!productoModificado.codigo || !productoModificado.nombre || !productoModificado.talle || !productoModificado.color || !productoModificado.stock) {
    return res.status(400).send('Datos de producto inválidos');
  }

  productoClient.ModificarProducto(productoModificado, (error, response) => {
    if (error) {
      console.error('Error modificando producto:', error.message);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.NOT_FOUND) {
        return res.status(404).send('Producto no encontrado');
      } else if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error modificando producto');
      }
    } else {
      res.status(200).json(response.producto);
    }
  });
});

// Ruta para borrar un producto
app.delete('/borrarProducto/:id', (req, res) => {
  const idProducto = req.params.id;

  productoClient.BorrarProducto({ id_producto: idProducto }, (error, response) => {
    if (error) {
      console.error('Error borrando producto:', error.message);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.NOT_FOUND) {
        return res.status(404).send('Producto no encontrado');
      } else if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error borrando producto');
      }
    } else {
      res.status(200).send('Producto borrado con éxito');
    }
  });
});
// Función para probar BorrarProducto
function borrarProducto(idProducto) {
  productoClient.BorrarProducto({ id_producto: idProducto }, (error, response) => {
    if (error) {
      console.error('Error borrando producto:', error);
    } else {
      console.log('Producto borrado con éxito:', response.producto);
    }
  });
}

/* Ruta para buscar un producto por nombre - TBD
app.get('/buscarProducto/:nombre', (req, res) => {
  const nombreProducto = req.params.nombre;

  productoClient.BuscarProducto({ nombre: nombreProducto }, (error, response) => {
    if (error) {
      console.error('Error buscando producto:', error.message);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.NOT_FOUND) {
        return res.status(404).send('Producto no encontrado');
      } else if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error buscando producto');
      }
    } else if (response.producto) {
      res.status(200).json(response.producto);
    } else {
      res.status(404).send('Producto no encontrado');
    }
  });
});
// Función para probar BuscarProducto por nombre
function buscarProducto(nombreProducto) {
  productoClient.BuscarProducto({ nombre: nombreProducto }, (error, response) => {
    if (error) {
      console.error('Error buscando producto:', error);
    } else if (response.producto) {
      console.log('Producto encontrado:', response.producto);
    } else {
      console.log('Producto no encontrado');
    }
  });
}´*/

// Ruta para enlistar productos
app.get('/enlistarProductos', (req, res) => {
  productoClient.EnlistarProductos({}, (error, response) => {
    if (error) {
      console.error('Error enlistando productos:', error.message);

      // Manejar errores específicos de gRPC
      if (error.code === grpc.status.INVALID_ARGUMENT) {
        return res.status(400).send('Argumento inválido');
      } else {
        return res.status(500).send('Error enlistando productos');
      }
    } else {
      res.status(200).json(response.productos);
    }
  });
});
// Función para probar EnlistarProductos
function enlistarProductos() {
  productoClient.EnlistarProductos({}, (error, response) => {
    if (error) {
      console.error('Error enlistando productos:', error);
    } else {
      console.log('Productos encontrados:', response);
    }
  });
}

// Iniciar el servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Cliente escuchando en http://localhost:${PORT}`);
});


// Llamadas de prueba Tienda
// crearTienda(); //probado ok
// modificarTienda(2); // probado ok
// borrarTienda(2); // probado ok
// buscarTienda(3); // probado ok
// enlistarTiendas(); // probado ok
// buscarTiendaPorNombre('Mi Tienda'); //probado ok

// Llamadas de prueba usuario
// crearUsuario(); // probado ok
// modificarUsuario(2); // probado ok
// borrarUsuario(); // probado ok
// buscarUsuario("usuarioTest"); // Reemplazar con el nombre
// enlistarUsuarios(); // probado ok
// autenticarUsuario(); // probado ok

// Llamadas de prueba producto

// Llamadas de prueba Producto
// crearProducto(); // probar creación
// modificarProducto(1); // Descomentar y reemplazar con el ID real
// borrarProducto(1); // Descomentar y reemplazar con el ID real
// buscarProducto('Nuevo Nombre'); // Descomentar y reemplazar con el ID real
// enlistarProductos(); // probar listado
