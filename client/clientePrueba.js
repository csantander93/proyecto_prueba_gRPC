const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Ruta hacia el archivo .proto de la tienda
const STORE_PROTO_PATH = path.join(__dirname, 'proto', 'tienda.proto');
// Ruta hacia el archivo .proto de usuario
const USER_PROTO_PATH = path.join(__dirname, 'proto', 'usuario.proto');

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

// Obtener el paquete gRPC del archivo .proto
const tiendaProto = grpc.loadPackageDefinition(packageDefinition).tienda;
const userProto = grpc.loadPackageDefinition(userPackageDefinition).usuario;


// Crear un cliente para TiendaService
const tiendaClient = new tiendaProto.TiendaService('localhost:50051', grpc.credentials.createInsecure());
// Crear un cliente para UserService
const userClient = new userProto.UsuarioService('localhost:50051', grpc.credentials.createInsecure());


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
    username: 'usuarioTest2',
    password: 'passwordSeguro2',
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
  console.log('Buscando usuario con username:', username); // Imprime el username que se va a buscar
  userClient.BuscarUsuario({ username: username }, (error, response) => {
    if (error) {
      console.error('Error buscando usuario:', error);
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
      console.error('Error enlistando usuarios:', error);
    } else {
      console.log('Usuarios encontrados:', response);
    }
  });
}

// Función para probar AutenticarUsuario
function autenticarUsuario() {
  const credenciales = {
    username: 'usuarioTest',
    password: 'passwordSeguro'
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

// Llamadas de prueba
//crearTienda();
//modificarTienda(2); // Asumiendo que el ID de la tienda es 20
//borrarTienda(2);
//buscarTienda(3);
//enlistarTiendas();
//buscarTiendaPorNombre('Santa');

// Llamadas de prueba
//crearUsuario();
//modificarUsuario(3); // Reemplazar con el ID real del usuario
//borrarUsuario(3); // Reemplazar con el ID real del usuario
buscarUsuario("usuarioTest"); // Reemplazar con el nombre
//enlistarUsuarios();
//autenticarUsuario();