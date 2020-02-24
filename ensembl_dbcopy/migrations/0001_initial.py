# Generated by Django 2.1.15 on 2020-02-20 15:25

from django.db import migrations, models
import django.db.models.deletion
import ensembl_production.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dbs2Exclude',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_schema', models.CharField(db_column='TABLE_SCHEMA', max_length=64)),
            ],
            options={
                'db_table': 'dbs_2_exclude',
            },
        ),
        migrations.CreateModel(
            name='DebugLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(blank=True, max_length=128, null=True)),
                ('sequence', models.IntegerField(blank=True, null=True)),
                ('function', models.CharField(blank=True, max_length=128, null=True)),
                ('value', models.TextField(blank=True, max_length=8192, null=True)),
            ],
            options={
                'db_table': 'debug_log',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(choices=[('Vertebrates', 'Vertebrates'), ('Microbes', 'Microbes'), ('Metazoa', 'Metazoa'), ('VectorBase', 'VectorBase'), ('Plants', 'Plants'), ('WormBase', 'WormBase'), ('Compara', 'Compara'), ('Production', 'Production')], default='Vertebrates', max_length=80)),
            ],
            options={
                'verbose_name': 'Group',
                'db_table': 'group',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('auto_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('port', models.IntegerField()),
                ('mysql_user', models.CharField(max_length=64)),
                ('virtual_machine', models.CharField(blank=True, max_length=255, null=True)),
                ('mysqld_file_owner', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Host',
                'db_table': 'host',
            },
        ),
        migrations.CreateModel(
            name='RequestJob',
            fields=[
                ('job_id', models.CharField(default=uuid.uuid1, editable=False, max_length=128, primary_key=True, serialize=False)),
                ('src_host', models.TextField(max_length=2048)),
                ('src_incl_db', ensembl_production.models.NullTextField(blank=True, max_length=2048, null=True)),
                ('src_skip_db', ensembl_production.models.NullTextField(blank=True, max_length=2048, null=True)),
                ('src_incl_tables', ensembl_production.models.NullTextField(blank=True, max_length=2048, null=True)),
                ('src_skip_tables', ensembl_production.models.NullTextField(blank=True, max_length=2048, null=True)),
                ('tgt_host', models.TextField(max_length=2048)),
                ('tgt_db_name', ensembl_production.models.NullTextField(blank=True, max_length=2048, null=True)),
                ('tgt_directory', ensembl_production.models.NullTextField(blank=True, max_length=2048, null=True)),
                ('skip_optimize', models.BooleanField(default=False)),
                ('wipe_target', models.BooleanField(default=False)),
                ('convert_innodb', models.BooleanField(default=False)),
                ('email_list', models.TextField(blank=True, max_length=2048, null=True)),
                ('start_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('end_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('user', models.CharField(blank=True, max_length=64, null=True)),
                ('status', models.CharField(blank=True, editable=False, max_length=20, null=True)),
            ],
            options={
                'db_table': 'request_job',
            },
        ),
        migrations.CreateModel(
            name='TransferLog',
            fields=[
                ('auto_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tgt_host', models.CharField(editable=False, max_length=512)),
                ('table_schema', models.CharField(db_column='TABLE_SCHEMA', editable=False, max_length=64)),
                ('table_name', models.CharField(db_column='TABLE_NAME', editable=False, max_length=64)),
                ('renamed_table_schema', models.CharField(editable=False, max_length=64)),
                ('target_directory', models.TextField(blank=True, editable=False, max_length=2048, null=True)),
                ('start_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('end_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('size', models.BigIntegerField(blank=True, editable=False, null=True)),
                ('retries', models.IntegerField(blank=True, editable=False, null=True)),
                ('message', models.CharField(blank=True, editable=False, max_length=255, null=True)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, related_name='transfer_logs', to='ensembl_dbcopy.RequestJob')),
            ],
            options={
                'verbose_name': 'TransferLog',
                'db_table': 'transfer_log',
            },
        ),
        migrations.AlterUniqueTogether(
            name='host',
            unique_together={('name', 'port')},
        ),
        migrations.AddField(
            model_name='group',
            name='host_id',
            field=models.ForeignKey(db_column='auto_id', on_delete=django.db.models.deletion.CASCADE, to='ensembl_dbcopy.Host'),
        ),
        migrations.AlterUniqueTogether(
            name='transferlog',
            unique_together={('job_id', 'tgt_host', 'table_schema', 'table_name')},
        ),
    ]
