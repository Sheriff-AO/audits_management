from django.db.models import fields
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *


admin.site.register(Client)
admin.site.register(Vendor)
admin.site.register(Schedule)
admin.site.register(PageOne)
admin.site.register(PageTwo)
admin.site.register(PageThree)
admin.site.register(PageFour)
admin.site.register(PageFive)
admin.site.register(PageSix)
admin.site.register(PageSeven)






class ChecklistResource(resources.ModelResource):
    def get_export_headers(self):
        headers = []
        for field in self.get_export_fields():
            header = self.get_verbose_name(self.Meta.model, field.column_name)
            headers.append(header)
        return headers

    def get_verbose_name(self, model, column):
        """
        Takes a model and a particular column and returns a the verbose name for that column
        even when the column contains a foreign key to another model.
        """
        fields = column.split('__')

        for field_name in fields[:-1]:
            field = model._meta.get_field(field_name)

            if field.many_to_one:
                model = field.foreign_related_fields[0].model
            elif field.many_to_many or field.one_to_one or field.one_to_many:
                model = field.related_model
            else:
                raise ValueError('Incorrect column')

        return model._meta.get_field(fields[-1]).verbose_name


    class Meta:
        model = ChecklistForBank
        def genarate_fields_including_related_model(model):
            fields_in_model = []
            for field in model._meta.get_fields():
                if field.many_to_one:
                    model = field.foreign_related_fields[0].model
                if field.many_to_many or field.one_to_one or field.one_to_many:
                    model = field.related_model
                else:
                    # field is not a link to another model
                    fields_in_model.append(field.name)
                    continue
                fields_in_model += [f'{field.name}__{f.name}' for f in model._meta.get_fields()[1:] if f.name != 'id']
            return tuple(fields_in_model)

        fields = genarate_fields_including_related_model(model)
        exclude = ('id',)





class ChecklistResource_2(resources.ModelResource):
    def get_export_headers(self):
        headers = []
        for field in self.get_export_fields():
            header = self.get_verbose_name(self.Meta.model, field.column_name)
            headers.append(header)
        return headers

    def get_verbose_name(self, model, column):
        """
        Takes a model and a particular column and returns a the verbose name for that column
        even when the column contains a foreign key to another model.
        """
        fields = column.split('__')

        for field_name in fields[:-1]:
            field = model._meta.get_field(field_name)

            if field.many_to_one:
                model = field.foreign_related_fields[0].model
            elif field.many_to_many or field.one_to_one or field.one_to_many:
                model = field.related_model
            else:
                raise ValueError('Incorrect column')

        return model._meta.get_field(fields[-1]).verbose_name


    class Meta:
        model = ChecklistForFillingStation
        def genarate_fields_including_related_model(model):
            fields_in_model = []
            for field in model._meta.get_fields():
                if field.many_to_one:
                    model = field.foreign_related_fields[0].model
                if field.many_to_many or field.one_to_one or field.one_to_many:
                    model = field.related_model
                else:
                    # field is not a link to another model
                    fields_in_model.append(field.name)
                    continue
                fields_in_model += [f'{field.name}__{f.name}' for f in model._meta.get_fields()[1:] if f.name != 'id']
            return tuple(fields_in_model)

        fields = genarate_fields_including_related_model(model)
        exclude = ('id',)





class ChecklistResource_3(resources.ModelResource):
    def get_export_headers(self):
        headers = []
        for field in self.get_export_fields():
            header = self.get_verbose_name(self.Meta.model, field.column_name)
            headers.append(header)
        return headers

    def get_verbose_name(self, model, column):
        """
        Takes a model and a particular column and returns a the verbose name for that column
        even when the column contains a foreign key to another model.
        """
        fields = column.split('__')

        for field_name in fields[:-1]:
            field = model._meta.get_field(field_name)

            if field.many_to_one:
                model = field.foreign_related_fields[0].model
            elif field.many_to_many or field.one_to_one or field.one_to_many:
                model = field.related_model
            else:
                raise ValueError('Incorrect column')

        return model._meta.get_field(fields[-1]).verbose_name


    class Meta:
        model = ChecklistForCandI
        def genarate_fields_including_related_model(model):
            fields_in_model = []
            for field in model._meta.get_fields():
                if field.many_to_one:
                    model = field.foreign_related_fields[0].model
                if field.many_to_many or field.one_to_one or field.one_to_many:
                    model = field.related_model
                else:
                    # field is not a link to another model
                    fields_in_model.append(field.name)
                    continue
                fields_in_model += [f'{field.name}__{f.name}' for f in model._meta.get_fields()[1:] if f.name != 'id']
            return tuple(fields_in_model)

        fields = genarate_fields_including_related_model(model)
        exclude = ('id',)





@admin.register(ChecklistForBank)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = ChecklistResource

@admin.register(ChecklistForFillingStation)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = ChecklistResource_2

@admin.register(ChecklistForCandI)
class ViewAdmin(ImportExportModelAdmin):
    resource_class = ChecklistResource_3


@admin.register(Site)
class ImportSite(ImportExportModelAdmin):
    pass

