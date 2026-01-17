def tenant_create_save(obj,user=None,company=None, branch=None):
    try:
        # obj.company_name = company
        # obj.branch_name = branch
        obj.created_by = user
        obj.updated_by = user
        obj.save()
        return True
    except Exception as error:
        print('Error : ', error)
        return False

def pre_setup_tenant_create_save(obj,user=None):
    try:
        obj.created_by = user
        # obj.updated_by_id = user.pk
        obj.save()
        return True
    except Exception as error:
        print('Error : ', error)
        return False
