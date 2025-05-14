# app/validators/evaluation_validator.py

from app.models.evaluation_type import EvaluationType

def assign_default_ponderations(evaluation_type, evaluations):
    if not all(data['ponderation'] is None for data in evaluations):
        return None

    if evaluation_type.ponderation_type == 'Peso':
        for data in evaluations:
            data['ponderation'] = 1
        return None

    existing_percentage_sum = round(
        sum(
            (evaluation.ponderation or 0)
            for evaluation in evaluation_type.evaluations
        ),
        2
    )
    remaining_percentage = round(100 - existing_percentage_sum, 2)
    amount_of_evaluations_being_created = len(evaluations)

    if remaining_percentage <= 0:
        return 'No queda porcentaje disponible para repartir.'

    percentage_each_evaluation = round(
        remaining_percentage / amount_of_evaluations_being_created, 2
    )
    for index, data in enumerate(evaluations):
        if index < amount_of_evaluations_being_created - 1:
            data['ponderation'] = percentage_each_evaluation
        else:
            data['ponderation'] = round(
                remaining_percentage 
                - percentage_each_evaluation 
                * (amount_of_evaluations_being_created - 1), 2
            )

    return None
