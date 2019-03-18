# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_mysql.models import EnumField
from multiselectfield import MultiSelectField

DB_TYPE_CHOICES_BIOTYPE = (('cdna', 'cdna'),
                           ('core', 'core'),
                           ('coreexpressionatlas', 'coreexpressionatlas'),
                           ('coreexpressionest', 'coreexpressionest'),
                           ('coreexpressiongnf', 'coreexpressiongnf'),
                           ('funcgen', 'funcgen'),
                           ('otherfeatures', 'otherfeatures'),
                           ('rnaseq', 'rnaseq'),
                           ('variation', 'variation'),
                           ('vega', 'vega'),
                           ('presite', 'presite'),
                           ('sangervega', 'sangervega'))

DB_TYPE_CHOICES_METAKEY = (('cdna', 'cdna'),
                           ('compara', 'compara'),
                           ('core', 'core'),
                           ('funcgen', 'funcgen'),
                           ('otherfeatures', 'otherfeatures'),
                           ('rnaseq', 'rnaseq'),
                           ('variation', 'variation'),
                           ('vega', 'vega'),
                           ('presite', 'presite'),
                           ('sangervega', 'sangervega'))


class BaseTimestampedModel(models.Model):
    """
    Time stamped 'able' models objects, add fields to inherited objects
    """

    class Meta:
        abstract = True
        app_label = 'ensembl_production'
        ordering = ['-updated', '-created']

    #: created by user (external DB ID)
    created_by = models.IntegerField(blank=True, null=True)
    #: (auto_now_add): set when model object is created
    created_at = models.DateTimeField('Created on', auto_now_add=True, editable=False, null=True,
                                      help_text='Creation timestamp')
    #: Modified by user (external DB ID)
    modified_by = models.IntegerField(blank=True, null=True)
    #: (auto_now): set each time model object is saved in database
    modified_at = models.DateTimeField('Last Update', auto_now=True, editable=False, null=True,
                                       help_text='Last update timestamp')


class HasCurrent(models.Model):
    class Meta:
        abstract = True
        app_label = 'ensembl_production'

    is_current = models.BooleanField(default=True)


class WebData(BaseTimestampedModel):
    web_data_id = models.AutoField(primary_key=True)
    data = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'ensembl_production'
        db_table = 'web_data'
        verbose_name = 'WebData'

    def __str__(self):
        return 'WebData: {}'.format(self.data)


class AnalysisDescription(HasCurrent, BaseTimestampedModel):
    analysis_description_id = models.AutoField(primary_key=True)
    logic_name = models.CharField(unique=True, max_length=128)
    description = models.TextField(blank=True, null=True)
    display_label = models.CharField(max_length=256)
    db_version = models.BooleanField(default=True)
    web_data = models.ForeignKey(WebData, null=True, blank=True, on_delete=models.SET_NULL)
    displayable = models.BooleanField(default=True)

    class Meta:
        db_table = 'analysis_description'
        app_label = 'ensembl_production'


class MasterAttribType(HasCurrent, BaseTimestampedModel):
    attrib_type_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'master_attrib_type'
        app_label = 'ensembl_production'
        verbose_name = 'AttribType'

    def __str__(self):
        return 'AttribType: {}'.format(self.name)


class MasterAttrib(HasCurrent, BaseTimestampedModel):
    attrib_id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=80)
    attrib_type = models.ForeignKey(MasterAttribType, db_column='attrib_type_id', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'master_attrib'
        app_label = 'ensembl_production'
        verbose_name = 'Attrib'

    def __str__(self):
        return 'Attrib: {}'.format(self.value)


class MasterAttribSet(HasCurrent, BaseTimestampedModel):
    attrib_set_id = models.IntegerField()
    attrib = models.OneToOneField(MasterAttrib, db_column='attrib_id', on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = 'master_attrib_set'
        app_label = 'ensembl_production'
        verbose_name = 'AttribSet'


class MasterBiotype(HasCurrent, BaseTimestampedModel):
    biotype_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    is_dumped = models.BooleanField(default=True)
    object_type = EnumField(choices=['gene', 'transcript'], default='gene')
    db_type = MultiSelectField(choices=DB_TYPE_CHOICES_BIOTYPE, default='core')
    description = models.TextField(blank=True, null=True)
    biotype_group = EnumField(
        choices=['coding', 'pseudogene', 'snoncoding', 'lnoncoding', 'mnoncoding', 'LRG', 'undefined', 'no_group'],
        default='no_group')
    so_acc = models.CharField(max_length=64, blank=True, null=True)
    so_term = models.CharField(max_length=1023, blank=True, null=True)
    attrib_type = models.ForeignKey(MasterAttribType, db_column='attrib_type_id', blank=True, null=True,
                                    on_delete=models.SET_NULL)

    class Meta:
        db_table = 'master_biotype'
        app_label = 'ensembl_production'
        unique_together = (('name', 'object_type'),)
        verbose_name = 'Biotype'


class MasterExternalDb(HasCurrent, BaseTimestampedModel):
    external_db_id = models.AutoField(primary_key=True)
    db_name = models.CharField(max_length=100)
    db_release = models.CharField(max_length=255, blank=True, null=True)
    status = EnumField(choices=['KNOWNXREF', 'KNOWN', 'XREF', 'PRED', 'ORTH', 'PSEUDO'])
    priority = models.IntegerField()
    db_display_name = models.CharField(max_length=255)
    type = EnumField(choices=['ARRAY', 'ALT_TRANS', 'ALT_GENE', 'MISC', 'LIT', 'PRIMARY_DB_SYNONYM', 'ENSEMBL'])
    secondary_db_name = models.CharField(max_length=255, blank=True, null=True)
    secondary_db_table = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'master_external_db'
        app_label = 'ensembl_production'
        unique_together = (('db_name', 'db_release', 'is_current'),)
        verbose_name = 'ExternalDB'


class MasterMiscSet(HasCurrent, BaseTimestampedModel):
    misc_set_id = models.PositiveSmallIntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=25)
    name = models.CharField(max_length=255)
    description = models.TextField()
    max_length = models.PositiveIntegerField()

    class Meta:
        app_label = 'ensembl_production'
        db_table = 'master_misc_set'


class MasterUnmappedReason(HasCurrent, BaseTimestampedModel):
    unmapped_reason_id = models.AutoField(primary_key=True)
    summary_description = models.CharField(max_length=255, blank=True, null=True)
    full_description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'ensembl_production'
        db_table = 'master_unmapped_reason'


class MetaKey(HasCurrent, BaseTimestampedModel):
    meta_key_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    is_optional = models.BooleanField(default=False)
    db_type = MultiSelectField(choices=DB_TYPE_CHOICES_METAKEY)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'meta_key'
        app_label = 'ensembl_production'
