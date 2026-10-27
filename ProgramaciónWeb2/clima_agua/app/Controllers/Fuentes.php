<?php
namespace App\Controllers;
use App\Models\FuenteModel;
use CodeIgniter\Exceptions\PageNotFoundException;

class Fuentes extends BaseController
{
    protected $helpers = ['url', 'form'];

    private function resultados(): array
    {
        $modelo = new FuenteModel();
        $q = trim((string) $this->request->getGet('q'));
        $categoria = (string) $this->request->getGet('categoria');
        $ambito = (string) $this->request->getGet('ambito');
        $fuentes = $modelo->catalogo($q, $categoria, $ambito)->paginate(5);
        // Los enlaces siempre abren una página completa, incluso desde el parcial AJAX.
        $modelo->pager->setPath(parse_url(site_url('fuentes'), PHP_URL_PATH));
        return ['fuentes' => $fuentes, 'pager' => $modelo->pager, 'q' => $q,
            'categoriaSeleccionada' => $categoria, 'ambitoSeleccionado' => $ambito];
    }

    private function opciones(): array
    {
        $db = db_connect();
        return ['categorias' => $db->table('categorias')->orderBy('nombre')->get()->getResultArray(),
            'ambitos' => $db->table('ambitos')->orderBy('nombre')->get()->getResultArray(),
            'variables' => $db->table('variables')->orderBy('nombre')->get()->getResultArray()];
    }

    public function index()
    {
        return view('fuentes/index', array_merge($this->resultados(), $this->opciones(), ['titulo' => 'Fuentes de datos']));
    }

    public function buscarAjax()
    {
        // Se devuelve solamente la tabla y el paginador como HTML parcial.
        return $this->response->setHeader('Cache-Control', 'no-store')->setBody(view('fuentes/tabla', $this->resultados()));
    }

    private function encontrar(int $id): array
    {
        $fuente = (new FuenteModel())->catalogo()->find($id);
        if (!$fuente) throw PageNotFoundException::forPageNotFound('La fuente no existe.');
        return $fuente;
    }

    public function crear()
    {
        return view('fuentes/crear', array_merge($this->opciones(), ['titulo' => 'Registrar fuente', 'fuente' => []]));
    }

    public function ver(int $id)
    {
        return view('fuentes/ver', ['titulo' => 'Detalle de fuente', 'fuente' => $this->encontrar($id)]);
    }

    public function editar(int $id)
    {
        return view('fuentes/editar', array_merge($this->opciones(), ['titulo' => 'Editar fuente', 'fuente' => $this->encontrar($id)]));
    }

    private function datosValidos(): ?array
    {
        $reglas = [
            'nombre' => 'required|max_length[150]', 'institucion' => 'required|max_length[200]',
            'descripcion' => 'permit_empty|max_length[5000]',
            'categoria_id' => 'required|is_natural_no_zero|is_not_unique[categorias.id]',
            'ambito_id' => 'required|is_natural_no_zero|is_not_unique[ambitos.id]',
            'variable_id' => 'required|is_natural_no_zero|is_not_unique[variables.id]',
            'url' => 'permit_empty|valid_url_strict[http,https]|max_length[500]',
            'tipo_acceso' => 'required|in_list[Libre,Registro requerido,Solicitud institucional,Por verificar]',
            'estado' => 'required|in_list[Activo,Inactivo]',
        ];
        foreach (['cobertura','resolucion_espacial','resolucion_temporal','periodo_disponible','formato'] as $campo) {
            $reglas[$campo] = 'permit_empty|max_length[200]';
        }
        if (!$this->validateData($this->request->getPost(), $reglas)) return null;
        return $this->validator->getValidated();
    }

    public function guardar()
    {
        $datos = $this->datosValidos();
        if ($datos === null) return redirect()->to(site_url('fuentes/crear'))->withInput()->with('errores', $this->validator->getErrors());
        (new FuenteModel())->insert($datos);
        return redirect()->to(site_url('fuentes'))->with('mensaje', 'Fuente registrada correctamente.');
    }

    public function actualizar(int $id)
    {
        $this->encontrar($id);
        $datos = $this->datosValidos();
        if ($datos === null) return redirect()->to(site_url('fuentes/editar/' . $id))->withInput()->with('errores', $this->validator->getErrors());
        (new FuenteModel())->update($id, $datos);
        return redirect()->to(site_url('fuentes'))->with('mensaje', 'Fuente actualizada correctamente.');
    }

    public function eliminar(int $id)
    {
        $this->encontrar($id);
        (new FuenteModel())->delete($id);
        return redirect()->to(site_url('fuentes'))->with('mensaje', 'Fuente eliminada correctamente.');
    }

    public function variables()
    {
        return view('catalogos/index', ['titulo' => 'Variables', 'filas' => $this->opciones()['variables']]);
    }

    public function categorias()
    {
        return view('catalogos/index', ['titulo' => 'Categorías', 'filas' => $this->opciones()['categorias']]);
    }
}
