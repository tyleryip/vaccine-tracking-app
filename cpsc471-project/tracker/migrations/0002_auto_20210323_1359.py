# Generated by Django 3.1.7 on 2021-03-23 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='disposedat',
            options={'verbose_name': 'Vaccine Disposal (DisposedAt)', 'verbose_name_plural': 'Vaccine Disposals (DisposedAt)'},
        ),
        migrations.AlterModelOptions(
            name='storedat',
            options={'verbose_name': 'Vaccine Stockpile (StoredAt)', 'verbose_name_plural': 'Vaccine Stockpiles (StoredAt)'},
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='vaccination_site_address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccinationsite', verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='vaccine_DIN_no',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine', verbose_name='Vaccine'),
        ),
        migrations.AlterField(
            model_name='civilian',
            name='hcc_no',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Healthcare Card Number'),
        ),
        migrations.AlterField(
            model_name='civilian',
            name='phone_no',
            field=models.IntegerField(verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='disposedat',
            name='DIN_no',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine', verbose_name='Vaccine'),
        ),
        migrations.AlterField(
            model_name='disposedat',
            name='biohazard_leakage',
            field=models.BooleanField(default=True, verbose_name='Biohazard Leakage Risk'),
        ),
        migrations.AlterField(
            model_name='disposedat',
            name='disposed_at_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='disposedat',
            name='sharp',
            field=models.BooleanField(default=True, verbose_name='Sharp Risk'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='hcc_no',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Healthcare Card Number'),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='hcc_no',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Healthcare Card Number'),
        ),
        migrations.AlterField(
            model_name='ppe',
            name='is_disposable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='ppe',
            name='nurse_hcc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.nurse', verbose_name='Assigned Nurse'),
        ),
        migrations.AlterField(
            model_name='ppe',
            name='ppe_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ppe',
            name='supplier_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.ppesupplier', verbose_name='Supplier'),
        ),
        migrations.AlterField(
            model_name='riskfactor',
            name='at_risk_age',
            field=models.BooleanField(default=False, verbose_name='High-Risk Age Bracket (>70)'),
        ),
        migrations.AlterField(
            model_name='riskfactor',
            name='location',
            field=models.BooleanField(default=False, verbose_name='High-Risk Location'),
        ),
        migrations.AlterField(
            model_name='riskfactor',
            name='occupation',
            field=models.BooleanField(default=False, verbose_name='High-Risk Occupation (Health Care)'),
        ),
        migrations.AlterField(
            model_name='storedat',
            name='DIN_no',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine', verbose_name='Vaccine'),
        ),
        migrations.AlterField(
            model_name='storedat',
            name='humidity',
            field=models.FloatField(default=60, verbose_name='Humidity (%)'),
        ),
        migrations.AlterField(
            model_name='storedat',
            name='lighting',
            field=models.FloatField(default=0, verbose_name='Light Level (Lumens)'),
        ),
        migrations.AlterField(
            model_name='storedat',
            name='stored_at_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='storedat',
            name='temperature',
            field=models.FloatField(default=20, verbose_name='Storage Temp (°C)'),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='DIN_no',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='DIN (Drug Identification Number)'),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='expiry_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='vaccinesideeffect',
            name='side_effect_name',
            field=models.CharField(max_length=200, verbose_name='Side Effect'),
        ),
        migrations.AlterField(
            model_name='vaccinesideeffect',
            name='vaccine_DIN_no',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine', verbose_name='Vaccine'),
        ),
        migrations.AlterField(
            model_name='vaccinesideeffect',
            name='vaccine_side_effect_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
