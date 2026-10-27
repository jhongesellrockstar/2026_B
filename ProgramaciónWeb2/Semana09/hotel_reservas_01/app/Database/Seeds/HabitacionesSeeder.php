<?php

namespace App\Database\Seeds;

use CodeIgniter\Database\Seeder;

class HabitacionesSeeder extends Seeder
{
    public function run()
    {
        $habitaciones = [
            ['codigo' => 'H101', 'tipo' => 'sencilla', 'capacidad' => 1, 'precio_noche' => 100, 'estado' => 'disponible', 'fecha' => '2026-10-27'],
            ['codigo' => 'H102', 'tipo' => 'doble', 'capacidad' => 2, 'precio_noche' => 200, 'estado' => 'ocupada', 'fecha' => '2026-10-27'],
            ['codigo' => 'H103', 'tipo' => 'triple', 'capacidad' => 3, 'precio_noche' => 300, 'estado' => 'mantenimiento', 'fecha' => '2026-10-27'],
        ];
        foreach ($habitaciones as $habitacion) {
            if (!$this->db->table('habitaciones')->where('codigo', $habitacion['codigo'])->countAllResults()) {
                $this->db->table('habitaciones')->insert($habitacion);
            }
        }
    }
}
