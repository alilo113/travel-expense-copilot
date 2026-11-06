


def check_travel_policy(category, amount, employee_role='standard'):
    """
    Checks if the travel expense is compliant based on the employee's role and the expense category.

    Args:
        category (str): The expense category, either 'flight' or 'hotel'.
        amount (float): The cost of the expense in USD.
        employee_role (str): The employee's role, either 'standard' or 'executive'. Defaults to 'standard'.

    Returns:
        dict: A dictionary containing 'compliant', 'requires_human_approval', and 'message'.
    """

    policy_limits = {
        'standard': {'flight': 600.0, 'hotel': 200.0},
        'executive': {'flight': 1500.0, 'hotel': 500.0}
    }

    limit = policy_limits[employee_role][category]
    compliant = amount <= limit
    requires_human_approval = limit < amount <= limit * 1.2
    
    message = 'Compliant' if compliant else 'Requires human approval' if requires_human_approval else 'Non-compliant'

    return {
        'compliant': compliant,
        'requires_human_approval': requires_human_approval,
        'message': message
    }
