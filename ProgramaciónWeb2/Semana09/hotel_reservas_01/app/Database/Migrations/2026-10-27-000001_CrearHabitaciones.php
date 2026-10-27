<?php

namespace App\Database\Migrations;

use CodeIgniter\Database\Migration;

class CrearHabitaciones extends Migration
{
    public function up()
    {
        $this->forge->addField([
            'id' => ['type' => 'INT', 'unsigned' => true, 'auto_increment' => true],
            'codigo' => ['type' => 'VARCHAR', 'constraint' => 20],
            'tipo' => ['type' => 'ENUM', 'constraint' => ['sencilla', 'doble', 'triple']],
            'capacidad' => ['type' => 'INT', 'unsigned' => true],
            'precio_noche' => ['type' => 'DECIMAL', 'constraint' => '10,2', 'unsigned' => true],
            'estado' => ['type' => 'ENUM', 'constraint' => ['disponible', 'mantenimiento', 'ocupada']],
            'fecha' => ['type' => 'DATE'],
        ]);
        $this->forge->addKey('id', true);
        $this->forge->addUniqueKey('codigo');
        $this->forge->createTable('habitaciones', true);
    }

    public function down()
    {
        $this->forge->dropTable('habitaciones', true);
    }
}
