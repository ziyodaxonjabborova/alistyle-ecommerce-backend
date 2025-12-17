from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class DeliveryTime(models.IntegerChoices):
    ONE_TO_TWO_DAYS = 2, "1–2 days"
    THREE_TO_FIVE_DAYS = 5, "3–5 days"
    SEVEN_TO_TEN_DAYS = 10, "7–10 days"

    ONE_MONTH = 30, "1 month"
    TWO_MONTHS = 60, "2 months"
    THREE_MONTHS = 90, "3 months"


class ProductBrand(models.TextChoices):
    APPLE = "apple", "Apple"
    SAMSUNG = "samsung", "Samsung"
    NIKE = "nike", "Nike"
    ADIDAS = "adidas", "Adidas"
    COCA_COLA = "coca_cola", "Coca-Cola"
    PEPSI = "pepsi", "Pepsi"
    NESTLE = "nestle", "Nestlé"
    IKEA = "ikea", "IKEA"
    LOREAL = "loreal", "L'Oréal"
    PUMA = "puma", "Puma"
    SONY = "sony", "Sony"
    LG = "lg", "LG"


class ProductSize(models.TextChoices):
    XS = "XS", "XS"
    S = "S", "S"
    M = "M", "M"
    L = "L", "L"
    XL = "XL", "XL"
    XXL = "XXL", "XXL"

    SIZE_36 = "36", "36"
    SIZE_37 = "37", "37"
    SIZE_38 = "38", "38"
    SIZE_39 = "39", "39"
    SIZE_40 = "40", "40"
    SIZE_41 = "41", "41"
    SIZE_42 = "42", "42"

    FREE_SIZE = "free", "Free Size"


class ColorChoices(models.TextChoices):
    WHITE = "white", "White"
    BLACK = "black", "Black"
    RED = "red", "Red"
    BLUE = "blue", "Blue"
    GREEN = "green", "Green"
    YELLOW = "yellow", "Yellow"
    ORANGE = "orange", "Orange"
    PINK = "pink", "Pink"
    PURPLE = "purple", "Purple"
    GREY = "grey", "Grey"
    BROWN = "brown", "Brown"
    GOLD = "gold", "Gold"
    SILVER = "silver", "Silver"


class ProductCondition(models.TextChoices):
    NEW = "new", "New"
    USED = "used", "Used"
    REFURBISHED = "refurbished", "Refurbished"
    DAMAGED = "damaged", "Damaged"
    LIKE_NEW = "like_new", "Like New"


class Country(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.FileField(upload_to="images/countries_icons")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            number = 1
            original_slug = slug
            while Country.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{number}"
                number += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.FileField(upload_to="images/category")
    desc = models.TextField()
    view = models.PositiveBigIntegerField(default=0)
    color = models.CharField(max_length=100, choices=ColorChoices.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            number = 1
            original_slug = slug
            while Category.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{number}"
                number += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
   


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            number = 1
            original_slug = slug
            while ProductCategory.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{number}"
                number += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        
        
class Product(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    desc = models.TextField()
    main_image = models.FileField(upload_to="images/main_images")
    price = models.PositiveIntegerField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True) # SET_NULL uchun null=True
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    review = models.PositiveSmallIntegerField(default=0)
    year = models.PositiveSmallIntegerField()
    delivery_time = models.CharField(max_length=50, choices=DeliveryTime.choices)
    star = models.PositiveSmallIntegerField(default=0)
    company = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, choices=ProductBrand.choices)
    size = models.CharField(max_length=40, choices=ProductSize.choices) 
    discount = models.PositiveSmallIntegerField(default=0)
    color = models.CharField(max_length=50, choices=ColorChoices.choices) 
    verified = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)
    condition = models.CharField(max_length=60, choices=ProductCondition.choices) 
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            number = 1
            original_slug = slug
            while Product.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{number}"
                number += 1
            self.slug = slug
        
        
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        
    
        

class ProductImage(models.Model):
    image = models.FileField(upload_to="images/product_images")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} image" 

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
    
    

class Services(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.FileField(upload_to="images/services")
    desc = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            number = 1
            original_slug = slug
            while Services.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{number}"
                number += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"