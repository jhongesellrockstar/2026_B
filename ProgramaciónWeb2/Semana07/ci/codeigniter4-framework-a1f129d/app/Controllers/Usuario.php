<?php

namespace App\Controllers;

use App\Models\UsuarioModel;

class Usuario extends BaseController
{
    public function index()
    {
        $model = new UsuarioModel();
        // Obtenemos todos los registros de la tabla
        $data['usuarios'] = $model->findAll(); 

        // Cargamos la vista y le pasamos los datos


        return view("template/header")
        . view("template/navbar")
        . view('usuarios/listado', $data)
        . view("template/footer");



    }
}
