# Generated by Django 3.1.7 on 2021-04-12 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('tracker', '0001_initial'), ('tracker', '0002_auto_20210323_1359'), ('tracker', '0003_auto_20210323_2016'), ('tracker', '0004_auto_20210328_1339'), ('tracker', '0005_auto_20210328_1409'), ('tracker', '0006_auto_20210328_1414'), ('tracker', '0007_auto_20210328_1530')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Civilian',
            fields=[
                ('hcc_no', models.IntegerField(primary_key=True, serialize=False)),
                ('phone_no', models.IntegerField()),
                ('sex', models.CharField(max_length=1)),
                ('address', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DisposalSite',
            fields=[
                ('address', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('disposal_method', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('hcc_no', models.IntegerField(primary_key=True, serialize=False)),
                ('phone_no', models.IntegerField()),
                ('sex', models.CharField(max_length=1)),
                ('address', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('place_of_practice', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('hcc_no', models.IntegerField(primary_key=True, serialize=False)),
                ('phone_no', models.IntegerField()),
                ('sex', models.CharField(max_length=1)),
                ('address', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PpeSupplier',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('website', models.CharField(max_length=200)),
                ('contact_name', models.CharField(max_length=200)),
                ('contact_phone', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VaccinationSite',
            fields=[
                ('address', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('capacity', models.IntegerField()),
                ('contact_name', models.CharField(max_length=200)),
                ('contact_phone_no', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('DIN_no', models.IntegerField(primary_key=True, serialize=False)),
                ('disease_treated', models.CharField(max_length=200)),
                ('recommended_dose', models.CharField(max_length=200)),
                ('expiry_date', models.DateTimeField()),
                ('manufacturer_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RiskFactor',
            fields=[
                ('hcc_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='tracker.civilian')),
                ('location', models.CharField(max_length=200)),
                ('occupation', models.CharField(max_length=200)),
                ('at_risk_age', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='VaccineSideEffect',
            fields=[
                ('vaccine_side_effect_id', models.IntegerField(primary_key=True, serialize=False)),
                ('side_effect_name', models.CharField(max_length=200)),
                ('vaccine_DIN_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine')),
            ],
        ),
        migrations.CreateModel(
            name='StoredAt',
            fields=[
                ('stored_at_id', models.IntegerField(primary_key=True, serialize=False)),
                ('temperature', models.FloatField(default=20)),
                ('humidity', models.FloatField(default=60)),
                ('lighting', models.FloatField(default=0)),
                ('DIN_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine')),
                ('vaccination_site_address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccinationsite')),
            ],
        ),
        migrations.CreateModel(
            name='Ppe',
            fields=[
                ('ppe_id', models.IntegerField(primary_key=True, serialize=False)),
                ('is_disposable', models.BooleanField()),
                ('nurse_hcc', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.nurse')),
                ('supplier_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.ppesupplier')),
            ],
        ),
        migrations.AddField(
            model_name='nurse',
            name='site_address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccinationsite'),
        ),
        migrations.CreateModel(
            name='HealthCondition',
            fields=[
                ('health_condition_id', models.IntegerField(primary_key=True, serialize=False)),
                ('condition', models.CharField(max_length=200)),
                ('hcc_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.civilian')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorCertification',
            fields=[
                ('doctor_certification_id', models.IntegerField(primary_key=True, serialize=False)),
                ('certification', models.CharField(max_length=200)),
                ('doctor_hcc_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='DisposedAt',
            fields=[
                ('disposed_at_id', models.IntegerField(primary_key=True, serialize=False)),
                ('sharp', models.BooleanField(default=True)),
                ('biohazard_leakage', models.BooleanField(default=True)),
                ('DIN_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine')),
                ('disposal_site_address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.disposalsite')),
            ],
        ),
        migrations.AddField(
            model_name='civilian',
            name='doctor_hcc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.doctor'),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('appointment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField()),
                ('civilian_hcc_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.civilian')),
                ('nurse_hcc_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.nurse')),
                ('vaccination_site_address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccinationsite')),
                ('vaccine_DIN_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine')),
            ],
        ),
        migrations.AddConstraint(
            model_name='vaccinesideeffect',
            constraint=models.UniqueConstraint(fields=('vaccine_DIN_no', 'side_effect_name'), name='VaccineSideEffect PK'),
        ),
        migrations.AddConstraint(
            model_name='storedat',
            constraint=models.UniqueConstraint(fields=('DIN_no', 'vaccination_site_address'), name='StoredAt PK'),
        ),
        migrations.AddConstraint(
            model_name='disposedat',
            constraint=models.UniqueConstraint(fields=('DIN_no', 'disposal_site_address'), name='DisposedAt PK'),
        ),
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
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.DateTimeField(),
        ),
        migrations.RemoveConstraint(
            model_name='disposedat',
            name='DisposedAt PK',
        ),
        migrations.RemoveConstraint(
            model_name='storedat',
            name='StoredAt PK',
        ),
        migrations.RemoveConstraint(
            model_name='vaccinesideeffect',
            name='VaccineSideEffect PK',
        ),
        migrations.AlterField(
            model_name='civilian',
            name='doctor_hcc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.doctor'),
        ),
        migrations.AlterField(
            model_name='disposedat',
            name='DIN_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine', verbose_name='Vaccine'),
        ),
        migrations.AlterField(
            model_name='disposedat',
            name='disposal_site_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.disposalsite'),
        ),
        migrations.AlterField(
            model_name='doctorcertification',
            name='doctor_hcc_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.doctor'),
        ),
        migrations.AlterField(
            model_name='healthcondition',
            name='hcc_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.civilian'),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='site_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccinationsite'),
        ),
        migrations.AlterField(
            model_name='ppe',
            name='nurse_hcc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.nurse', verbose_name='Assigned Nurse'),
        ),
        migrations.AlterField(
            model_name='ppe',
            name='supplier_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.ppesupplier', verbose_name='Supplier'),
        ),
        migrations.AlterField(
            model_name='riskfactor',
            name='hcc_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='tracker.civilian'),
        ),
        migrations.AlterField(
            model_name='storedat',
            name='DIN_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine', verbose_name='Vaccine'),
        ),
        migrations.AlterField(
            model_name='storedat',
            name='vaccination_site_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccinationsite'),
        ),
        migrations.AlterField(
            model_name='vaccinesideeffect',
            name='vaccine_DIN_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine', verbose_name='Vaccine'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='disposedat',
            name='disposed_at_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ppe',
            name='ppe_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='storedat',
            name='stored_at_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='vaccinesideeffect',
            name='vaccine_side_effect_id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='civilian_hcc_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.civilian'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='nurse_hcc_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.nurse'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='vaccination_site_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccinationsite', verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='vaccine_DIN_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine', verbose_name='Vaccine'),
        ),
    ]
