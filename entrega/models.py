# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=100, blank=True, null=True)
    admin_password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Admin'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Billinginfo(models.Model):
    billing_id = models.AutoField(primary_key=True)
    customer = models.OneToOneField('Customer', models.DO_NOTHING, blank=True, null=True)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    credit_card_number = models.CharField(max_length=16, blank=True, null=True)
    credit_card_pin = models.CharField(max_length=4, blank=True, null=True)
    credit_card_exp_date = models.DateField(blank=True, null=True)
    bill_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BillingInfo'


class Cart(models.Model):
    customer = models.ForeignKey('Customer', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    num_of_products = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Cart'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    picture = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Category'


class Customer(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customer'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    required_date = models.DateTimeField(blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    freight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipper = models.ForeignKey('Shipper', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Order'


class Orderdetails(models.Model):
    order = models.ForeignKey(Order, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OrderDetails'


class Personalinfo(models.Model):
    personal_id = models.AutoField(primary_key=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PersonalInfo'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    supplier = models.ForeignKey('Supplier', models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    quantity_per_unit = models.CharField(max_length=100, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    units_in_order = models.IntegerField(blank=True, null=True)
    units_in_stock = models.IntegerField(blank=True, null=True)
    reorder_level = models.IntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    picture = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Product'


class Shipper(models.Model):
    shipper_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Shipper'


class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('User', models.DO_NOTHING, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_title = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Supplier'


class User(models.Model):
    personal_info = models.OneToOneField(Personalinfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'
