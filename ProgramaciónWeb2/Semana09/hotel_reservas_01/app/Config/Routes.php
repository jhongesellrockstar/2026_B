<?php
use CodeIgniter\Router\RouteCollection;
/** @var RouteCollection $routes */

$routes->setAutoRoute(false);
$routes->get('/', 'Habitaciones::index');
$routes->get('habitaciones', 'Habitaciones::index');
$routes->get('habitaciones/crear', 'Habitaciones::crear');
$routes->post('habitaciones/guardar', 'Habitaciones::guardar');
$routes->get('habitaciones/editar/(:num)', 'Habitaciones::editar/$1');
$routes->post('habitaciones/actualizar/(:num)', 'Habitaciones::actualizar/$1');
$routes->post('habitaciones/eliminar/(:num)', 'Habitaciones::eliminar/$1');
