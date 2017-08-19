def purchase_state_or_other(user):
    if not user.phone:
        return 'phone'

    if not user.first_name:
        return 'first_name'

    return 'purchase'