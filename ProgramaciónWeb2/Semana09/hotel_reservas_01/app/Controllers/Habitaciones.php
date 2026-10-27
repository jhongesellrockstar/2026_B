<?php

namespace App\Controllers;

use App\Models\HabitacionModel;
use CodeIgniter\Exceptions\PageNotFoundException;

class Habitaciones extends BaseController
{
    public function index()
    {
        $modelo = new HabitacionModel();
        $habitaciones = $modelo->orderBy('id', 'DESC')->findAll();
        return view('habitaciones/index', ['habitaciones' => $habitaciones]);
    }

    public function crear()
    {
        return view('habitaciones/crear');
    }

    public function guardar()
    {
        if (!$this->validate($this->reglas())) {
            return redirect()->back()->withInput()->with('errores', $this->validator->getErrors());
        }

        $modelo = new HabitacionModel();
        $modelo->insert($this->datosHabitacion());
        return redirect()->to(site_url('habitaciones'))->with('mensaje', 'Habitación registrada correctamente.');
    }

    public function editar(int $id)
    {
        $habitacion = (new HabitacionModel())->find($id);
        if (!$habitacion) {
            throw PageNotFoundException::forPageNotFound('La habitación no existe.');
        }
        return view('habitaciones/editar', ['habitacion' => $habitacion]);
    }

    public function actualizar(int $id)
    {
        $modelo = new HabitacionModel();
        if (!$modelo->find($id)) {
            throw PageNotFoundException::forPageNotFound('La habitación no existe.');
        }
        if (!$this->validate($this->reglas($id))) {
            return redirect()->back()->withInput()->with('errores', $this->validator->getErrors());
        }

        $modelo->update($id, $this->datosHabitacion());
        return redirect()->to(site_url('habitaciones'))->with('mensaje', 'Habitación actualizada correctamente.');
    }

    public function eliminar(int $id)
    {
        $modelo = new HabitacionModel();
        if (!$modelo->find($id)) {
            throw PageNotFoundException::forPageNotFound('La habitación no existe.');
        }
        $modelo->delete($id);
        return redirect()->to(site_url('habitaciones'))->with('mensaje', 'Habitación eliminada correctamente.');
    }

    private function datosHabitacion(): array
    {
        $tipo = $this->request->getPost('tipo');
        $capacidades = ['sencilla' => 1, 'doble' => 2, 'triple' => 3];
        $precios = ['sencilla' => 100, 'doble' => 200, 'triple' => 300];

        // El servidor calcula estos valores aunque se altere el formulario.
        return [
            'codigo' => trim($this->request->getPost('codigo')),
            'tipo' => $tipo,
            'capacidad' => $capacidades[$tipo],
            'precio_noche' => $precios[$tipo],
            'estado' => $this->request->getPost('estado'),
            'fecha' => $this->request->getPost('fecha'),
        ];
    }

    private function reglas(int $id = 0): array
    {
        return [
            'codigo' => [
                'rules' => "required|max_length[20]|regex_match[/^\\S(?:.*\\S)?$/]|is_unique[habitaciones.codigo,id,$id]",
                'errors' => [
                    'required' => 'El código es obligatorio.',
                    'max_length' => 'El código admite hasta 20 caracteres.',
                    'regex_match' => 'Evita espacios al principio o al final del código.',
                    'is_unique' => 'Ya existe una habitación con ese código.',
                ],
            ],
            'tipo' => [
                'rules' => 'required|in_list[sencilla,doble,triple]',
                'errors' => ['required' => 'Selecciona el tipo.', 'in_list' => 'El tipo debe ser sencilla, doble o triple.'],
            ],
            'estado' => [
                'rules' => 'required|in_list[disponible,mantenimiento,ocupada]',
                'errors' => ['required' => 'Selecciona el estado.', 'in_list' => 'El estado debe ser disponible, mantenimiento u ocupada.'],
            ],
            'fecha' => [
                'rules' => 'required|valid_date[Y-m-d]',
                'errors' => ['required' => 'La fecha es obligatoria.', 'valid_date' => 'Ingresa una fecha válida.'],
            ],
        ];
    }
}
