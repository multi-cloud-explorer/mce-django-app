# Generated by Django 3.0.5 on 2020-04-16 10:00

from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields
import mce_django_app.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('username', models.CharField(max_length=255, verbose_name='Username or Client ID')),
                ('password', django_cryptography.fields.encrypt(models.CharField(max_length=255, verbose_name='Password or Secret Key'))),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('resource_id', models.CharField(max_length=1024, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('provider', models.CharField(choices=[('aws', 'Aws'), ('azure', 'Azure'), ('gcp', 'Gcp'), ('vmware', 'Vmware')], max_length=255)),
                ('metas', mce_django_app.utils.JSONField(blank=True, default={}, null=True)),
                ('locked', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResourceEventChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('action', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=10)),
                ('changes', mce_django_app.utils.JSONField(blank=True, default=[], null=True)),
                ('old_object', mce_django_app.utils.JSONField(blank=True, default={}, null=True)),
                ('new_object', mce_django_app.utils.JSONField(blank=True, default={}, null=True)),
                ('diff', models.TextField(blank=True, null=True)),
                ('object_id', models.CharField(max_length=1024)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('provider', models.CharField(choices=[('aws', 'Aws'), ('azure', 'Azure'), ('gcp', 'Gcp'), ('vmware', 'Vmware')], max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logger_name', models.CharField(max_length=100)),
                ('level', models.PositiveSmallIntegerField(choices=[(0, 'NotSet'), (20, 'Info'), (30, 'Warning'), (10, 'Debug'), (40, 'Error'), (50, 'Fatal')], db_index=True, default=40)),
                ('msg', models.TextField()),
                ('trace', models.TextField(blank=True, null=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Logging',
                'verbose_name_plural': 'Logging',
                'ordering': ('-create_datetime',),
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('subscription_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('tenant', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('is_china', models.BooleanField(default=False)),
                ('provider', models.CharField(choices=[('aws', 'Aws'), ('azure', 'Azure'), ('gcp', 'Gcp'), ('vmware', 'Vmware')], default='azure', editable=False, max_length=255)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_removed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('value', models.CharField(max_length=1024)),
                ('provider', models.CharField(blank=True, choices=[('aws', 'Aws'), ('azure', 'Azure'), ('gcp', 'Gcp'), ('vmware', 'Vmware')], max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceAzure',
            fields=[
                ('resource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mce_django_app.Resource')),
                ('kind', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(max_length=255)),
                ('sku', mce_django_app.utils.JSONField(blank=True, default={}, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('mce_django_app.resource',),
        ),
        migrations.CreateModel(
            name='ResourceGroupAzure',
            fields=[
                ('resource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mce_django_app.Resource')),
                ('location', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('mce_django_app.resource',),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('provider', 'name', 'value'), name='provider_name_value_uniq'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(condition=models.Q(provider__isnull=True), fields=('name', 'value'), name='name_value_without_provider_uniq'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions_azure', to='mce_django_app.GenericAccount'),
        ),
        migrations.AddField(
            model_name='resourceeventchange',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='resource',
            name='resource_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mce_django_app.ResourceType'),
        ),
        migrations.AddField(
            model_name='resource',
            name='tags',
            field=models.ManyToManyField(to='mce_django_app.Tag'),
        ),
        migrations.AddField(
            model_name='resourcegroupazure',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mce_django_app.Subscription'),
        ),
        migrations.AddField(
            model_name='resourceazure',
            name='resource_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mce_django_app.ResourceGroupAzure'),
        ),
        migrations.AddField(
            model_name='resourceazure',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mce_django_app.Subscription'),
        ),
    ]
