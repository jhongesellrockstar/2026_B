<?php

use CodeIgniter\Router\RouteCollection;

/** @var RouteCollection $routes */
$routes->setAutoRoute(false);
$routes->get('/', 'Fuentes::index');
$routes->get('fuentes', 'Fuentes::index');
$routes->get('fuentes/buscar', 'Fuentes::buscarAjax');
$routes->get('fuentes/crear', 'Fuentes::crear');
$routes->post('fuentes/guardar', 'Fuentes::guardar');
$routes->get('fuentes/ver/(:num)', 'Fuentes::ver/$1');
$routes->get('fuentes/editar/(:num)', 'Fuentes::editar/$1');
$routes->post('fuentes/actualizar/(:num)', 'Fuentes::actualizar/$1');
$routes->post('fuentes/eliminar/(:num)', 'Fuentes::eliminar/$1');
$routes->get('variables', 'Fuentes::variables');
$routes->get('categorias', 'Fuentes::categorias');
