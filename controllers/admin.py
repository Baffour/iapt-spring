# IAPT Spring Assessment - Group 13

def erase_db():
    form = FORM.confirm("Wipe the database")
    if form.accepted:
        for table in db.tables():
            try: db[table].drop()
            except: pass
        db.commit()
        session.clear()
        response.flash = 'All data erased'
        response.flash_type = 'success'
    return dict(form=form)
