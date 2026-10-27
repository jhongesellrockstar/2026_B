<?php

namespace App\Models;

use CodeIgniter\Model;

class HabitacionModel extends Model
{
    protected $table = 'habitaciones';
    protected $primaryKey = 'id';
    protected $returnType = 'array';
    protected $useTimestamps = false;
    protected $allowedFields = ['codigo', 'tipo', 'capacidad', 'precio_noche', 'estado', 'fecha'];
}
