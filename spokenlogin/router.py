class SpokenRouter:
    
    def db_for_read(self, model, **hints):
        if model._meta.db_table == 'website_question' or model._meta.db_table == 'website_answer':
            return 'forums'
        if model._meta.app_label == 'spokenlogin':
            return 'spk'
        if model._meta.app_label == 'cdcontent':
            return 'spk'
        
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'spokenlogin':
            return 'spk'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True