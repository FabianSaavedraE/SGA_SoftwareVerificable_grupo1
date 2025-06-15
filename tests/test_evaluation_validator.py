from app.validators import evaluation_validator as validator

def test_assign_default_ponderations_with_existing_values():
    evaluations = [{"ponderation": 10}]
    result = validator.assign_default_ponderations(None, evaluations)

    assert result is None
    assert evaluations[0]['ponderation'] == 10

def test_assign_default_ponderations_weight_type():
    evaluations = [{"ponderation": None}, {"ponderation": None}]
    eval_type = type("EvalType", (), {"ponderation_type": "Peso"})()
    result = validator.assign_default_ponderations(eval_type, evaluations)

    assert result is None
    for e in evaluations:
        assert e['ponderation'] == 1

def test_assign_default_ponderations_percentage_distribution():
    class EvaluationMock:
        def __init__(self, ponderation):
            self.ponderation = ponderation

    eval_type = type("EvalType", (), {
        "ponderation_type": "Porcentaje",
        "evaluations": [EvaluationMock(40)]
    })()

    evaluations = [{"ponderation": None}, {"ponderation": None}]
    result = validator.assign_default_ponderations(eval_type, evaluations)

    assert result is None
    assert round(sum(e['ponderation'] for e in evaluations), 2) == 60.0

def test_assign_default_ponderations_no_percentage_left():
    class EvaluationMock:
        def __init__(self, ponderation):
            self.ponderation = ponderation

    eval_type = type("EvalType", (), {
        "ponderation_type": "Porcentaje",
        "evaluations": [EvaluationMock(100)]
    })()

    evaluations = [{"ponderation": None}]
    result = validator.assign_default_ponderations(eval_type, evaluations)

    assert result == 'No queda porcentaje disponible para repartir.'
