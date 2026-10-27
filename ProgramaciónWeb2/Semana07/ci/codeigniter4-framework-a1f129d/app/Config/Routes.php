<?php

use CodeIgniter\Router\RouteCollection;

/** @var RouteCollection $routes */
$routes->get('/', 'Home::index');
$routes->get('/holamundo', 'Home::holamundo');



// USUARIOS
$routes->get('usuarios', 'Usuario::index');
