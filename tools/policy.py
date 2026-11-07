from langchain_core import tools

@tools
def policy_tool(category, amount, employee_role='standard'):

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