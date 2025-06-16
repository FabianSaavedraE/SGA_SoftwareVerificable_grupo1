from app.controllers import evaluation_controller


def test_convert_records_to_excel_returns_buffer():
    records = [
        {
            'Curso': 'Diseño de Software Verificable',
            'Seccion': 'NRC1001',
            'Tipo de Evaluación': 'Prueba',
            'Evaluación': 'Prueba 1',
            'Estudiante': 'Pedro Perez',
            'Nota': 5.5,
        }
    ]

    buffer = evaluation_controller.convert_records_to_excel(records)

    assert buffer is not None
    assert hasattr(buffer, 'read')


def test_convert_records_to_excel_returns_none_if_no_records():
    result = evaluation_controller.convert_records_to_excel([])

    assert result is None
