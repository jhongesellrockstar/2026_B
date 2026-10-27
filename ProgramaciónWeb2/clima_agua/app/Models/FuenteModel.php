<?php
namespace App\Models;
use CodeIgniter\Model;

class FuenteModel extends Model
{
    protected $table = 'fuentes';
    protected $primaryKey = 'id';
    protected $returnType = 'array';
    protected $useTimestamps = true;
    protected $allowedFields = ['nombre','institucion','descripcion','categoria_id','ambito_id','variable_id',
        'cobertura','resolucion_espacial','resolucion_temporal','periodo_disponible','formato','tipo_acceso','url','estado'];

    // Consulta compartida entre el listado normal y el buscador AJAX.
    public function catalogo(string $texto = '', string $categoria = '', string $ambito = '')
    {
        $this->select('fuentes.*, categorias.nombre AS categoria, ambitos.nombre AS ambito, variables.nombre AS variable')
            ->join('categorias', 'categorias.id = fuentes.categoria_id')
            ->join('ambitos', 'ambitos.id = fuentes.ambito_id')
            ->join('variables', 'variables.id = fuentes.variable_id', 'left');
        if ($texto !== '') {
            $this->groupStart()->like('fuentes.nombre', $texto)->orLike('fuentes.institucion', $texto)
                ->orLike('fuentes.cobertura', $texto)->orLike('variables.nombre', $texto)
                ->orLike('fuentes.descripcion', $texto)->groupEnd();
        }
        if (ctype_digit($categoria)) $this->where('fuentes.categoria_id', $categoria);
        if (ctype_digit($ambito)) $this->where('fuentes.ambito_id', $ambito);
        return $this->orderBy('fuentes.id', 'ASC');
    }
}
