"""Plantilla para crear un nuevo pipeline con arquitectura medallion."""

from typing import Dict, Any, Optional

from medallion_etl.core import MedallionPipeline
from medallion_etl.bronze import CSVExtractor
from medallion_etl.silver import SchemaValidator, DataCleaner
from medallion_etl.gold import Aggregator
from medallion_etl.schemas import BaseSchema
from medallion_etl.config import config

# Definir esquema de datos
class SampleSchema(BaseSchema):
    """Esquema de ejemplo para validación de datos."""
    # Definir campos aqu
    # id: int
    # name: str
    # value: float
    # date: datetime
    pass

# Definir pipeline
def create_sample_pipeline(name: str = "SamplePipeline") -> MedallionPipeline:
    """Crea un pipeline de ejemplo con arquitectura medallion."""
    pipeline = MedallionPipeline(name=name, description="Pipeline de ejemplo con arquitectura medallion")
    
    # Capa Bronze - Extracción
    extractor = CSVExtractor(
        name="SampleExtractor",
        description="Extrae datos de un archivo CSV",
        output_path=config.bronze_dir / name,
        save_raw=True
    )
    pipeline.add_bronze_task(extractor)
    
    # Capa Silver - Validación
    validator = SchemaValidator(
        schema_model=SampleSchema,
        name="SampleValidator",
        description="Valida datos contra el esquema definido",
        output_path=config.silver_dir / name,
        save_validated=True
    )
    pipeline.add_silver_task(validator)
    
    cleaner = DataCleaner(
        name="SampleCleaner",
        description="Limpia los datos",
        output_path=config.silver_dir / name,
        drop_na=True,
        drop_duplicates=True
    )
    pipeline.add_silver_task(cleaner)
    
    # Capa Gold - Transformación
    aggregator = Aggregator(
        group_by=["column1"],  # Reemplazar con columnas reales
        aggregations={
            "column2": "sum",  # Reemplazar con columnas y agregaciones reales
            "column3": "mean"
        },
        name="SampleAggregator",
        description="Agrega los datos",
        output_path=config.gold_dir / name
    )
    pipeline.add_gold_task(aggregator)
    
    # Opcional: Carga en base de datos
    # loader = SQLLoader(
    #     table_name="sample_table",
    #     connection_string="sqlite:///data/sample.db",
    #     name="SampleLoader",
    #     description="Carga datos en una tabla SQL"
    # )
    # pipeline.add_gold_task(loader)
    
    return pipeline

# Ejecutar pipeline
def run_sample_pipeline(input_path: str) -> Dict[str, Any]:
    """Ejecuta el pipeline de ejemplo con los datos de entrada."""
    pipeline = create_sample_pipeline()
    result = pipeline.run(input_path)
    return result.metadata

# Registrar como flow de Prefect
def register_prefect_flow(input_path: Optional[str] = None) -> None:
    """Registra el pipeline como un flow de Prefect."""
    pipeline = create_sample_pipeline()
    flow = pipeline.as_prefect_flow()
    
    if input_path:
        flow(input_path)

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar directorios
    config.ensure_directories()
    
    # Ejecutar pipeline
    input_path = "data/sample.csv"  # Reemplazar con la ruta real
    metadata = run_sample_pipeline(input_path)
    print(f"Pipeline ejecutado con éxito. Metadatos: {metadata}")