# IAPT Spring Assessment - Group 13

def create_unfiled_box(form):
    db.box.insert(
        name="Unfiled",
        private=True,
        unfiled=True,
        auth_user=form.vars.id
    )

auth.settings.register_onaccept.append(create_unfiled_box)
