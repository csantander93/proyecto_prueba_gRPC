const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

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

// Función para probar CrearTienda
function crearTienda() {
  const nuevaTienda = {
    codigo: 'T123',
    nombre: 'Mi Tienda',
    direccion: '123 Calle Falsa',
    ciudad: 'Ciudad Falsa',
    provincia: 'Provincia Falsa',
    habilitada: true,
    casa_central: false,
  };

  tiendaClient.CrearTienda(nuevaTienda, (error, response) => {
    if (error) {
      console.error('Error creando tienda:', error);
    } else {
      console.log('Tienda creada con éxito:', response.tienda);
    }
  });
}

// Función para probar ModificarTienda
function modificarTienda(idTienda) {
  const tiendaModificada = {
    id_tienda: idTienda,
    codigo: 'T111',
    nombre: 'Tienda super duper Modificada',
    direccion: '456 Calle Falsa falsa',
    ciudad: 'Ciudad Falsa falsa',
    provincia: 'Provincia Falsa falsa',
    habilitada: true,
    casa_central: true,
  };

  tiendaClient.ModificarTienda(tiendaModificada, (error, response) => {
    if (error) {
      console.error('Error modificando tienda:', error);
    } else {
      console.log('Tienda modificada con éxito:', response.tienda);
    }
  });
}

// Función para probar BorrarTienda
function borrarTienda(idTienda) {
  tiendaClient.BorrarTienda({ id_tienda: idTienda }, (error, response) => {
    if (error) {
      console.error('Error borrando tienda:', error);
    } else {
      console.log('Tienda borrada con éxito:', response.tienda);
    }
  });
}

// Función para probar BuscarTienda
function buscarTienda(idTienda) {
  tiendaClient.BuscarTienda({ id_tienda: idTienda }, (error, response) => {
    if (error) {
      console.error('Error buscando tienda:', error);
    } else if (response.tienda) {
      console.log('Tienda encontrada:', response.tienda);
    } else {
      console.log('Tienda no encontrada');
    }
  });
}

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
        console.error('Error creando usuario:', error.message); // Detalles del error
    } else {
        console.log('Usuario creado con éxito:', response.usuario);
    }
});

}

// Función para probar ModificarUsuario
function modificarUsuario(idUsuario) {
  const usuarioModificado = {
    id_usuario: idUsuario,
    username: 'usuarioModificado',
    password: 'nuevoPasswordSeguro',
    habilitado: true,
    tienda_idtienda: 2
  };

  userClient.ModificarUsuario(usuarioModificado, (error, response) => {
    if (error) {
      console.error('Error modificando usuario:', error);
    } else {
      console.log('Usuario modificado con éxito:', response.usuario);
    }
  });
}

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

// Función para probar CrearProducto
function crearProducto() {
  const nuevoProducto = {
    codigo: 'P123',
    nombre: 'Nombre del Producto',  // Agregado: nombre del producto
    talle: 'M',
    foto: 'url_a_la_foto',
    color: 'rojo',
    stock: 50,
    id_tienda: 1  // Agregado: ID de la tienda
  };

  productoClient.CrearProducto(nuevoProducto, (error, response) => {
    if (error) {
      console.error('Error creando producto:', error);
    } else {
      console.log('Producto creado con éxito:', response.producto);
    }
  });
}

// Función para probar ModificarProducto
function modificarProducto(idProducto) {
  const productoModificado = {
    id_producto: idProducto,
    codigo: 'P111',
    nombre: 'Nuevo Nombre', // Agregado: nombre del producto
    talle: 'L',
    foto: 'nueva_url_a_la_foto',
    color: 'azul',
    stock: 100,
    id_tienda: 'ID_de_la_tienda' // Agregado: ID de la tienda
  };

  productoClient.ModificarProducto(productoModificado, (error, response) => {
    if (error) {
      console.error('Error modificando producto:', error);
    } else {
      console.log('Producto modificado con éxito:', response.producto);
    }
  });
}

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

// Función para probar BuscarProducto
function buscarProducto(idProducto) {
  productoClient.BuscarProducto({ id_producto: idProducto }, (error, response) => {
    if (error) {
      console.error('Error buscando producto:', error);
    } else if (response.producto) {
      console.log('Producto encontrado:', response.producto);
    } else {
      console.log('Producto no encontrado');
    }
  });
}

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

// Llamadas de prueba Tienda
//crearTienda(); //probado ok
//modificarTienda(2); // probado ok
//borrarTienda(2); // probado ok
//buscarTienda(3); // probado ok
//enlistarTiendas(); // probado ok
//buscarTiendaPorNombre('Santa'); //probado ok

// Llamadas de prueba usuario
crearUsuario(); // probado ok
//modificarUsuario(5); // probado ok
//borrarUsuario(5); // probado ok
//buscarUsuario("usuarioModificado"); // Reemplazar con el nombre
//enlistarUsuarios(); // probado ok
//autenticarUsuario(); // probado ok

// Llamadas de prueba producto

// Llamadas de prueba Producto
//crearProducto(); // probar creación
// modificarProducto(1); // Descomentar y reemplazar con el ID real
// borrarProducto(1); // Descomentar y reemplazar con el ID real
// buscarProducto(1); // Descomentar y reemplazar con el ID real
// enlistarProductos(); // probar listado