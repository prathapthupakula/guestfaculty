class GFFacultyName(models.Model):
    id= models.AutoField(primary_key =True,editable=False)
    computers=models.CharFiled(max_length=225,)
    mathematics=models.CharField(max_length=225)
    electronics=models.CharField(max_length=225)
    address=models.CharField(max_length=225,)
    phno=models.CharField(max_length=225,)
    email=models.CharField(max_length=225,)
    
    class Meta:
        managed=False
        db_table='facultyname'
        verbose_name = 'GFFacultyName'
        verbose_name_plural='GFFacultyName'





class GFEmployeeDetails(models.Model):
    emp_id =exmodels.Autofield(primary_key =True,editable=False)
    emp_name =exmodels.CharField(max_length=225,)
    mobile= exmodels.CharField(max_length=225,)
    email=exmodels.CharField(max_length=225,)
    emp_city=exmodels.CharField(max_length=225,)
    emp_state=exmodels.CharField(max_length=225,)
    pincode=exmodels.CharField(max_length=225,)
    
    class Meta:
        managed=False
        db_table='employee_details'
        verbose_name='GFEmployee Details'
        verbose_name_plural='GFEmployee Details'



class Example(models.Model):
    id = models.AutoField(primary_key =True,editable=False)
    name = models.CharField(max_length =225,)
    mobile = models.CharField(max_length =225,)
    email = models.CharField(max_Length = 225,)
    
    class Meta:
    managed = False
    db_table = 'gfnewtable'
    verbose_name = 'Example Table'
    verbose_name_plural = 'Eaxample Data'
