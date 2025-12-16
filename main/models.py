from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import shuffle, choices, randint
from string import ascii_letters, digits


class DeliveryTime(models.IntegerChoices):
    ONE_TO_TWO_DAYS=2, "1-2 days"
    THREE_TO_FIVE_DAYS=5, "3-5 days"
    SEVEN_TO_TEN_DAYS=10,  "7-10 days"
    
    ONE_MONTH=30,  "1 month"
    TWO_MONTH=60,  "2 month"
    THREE_MONTH=90, "3 month"


class ProductBrand(models.TextChoices):
    APPLE = "apple", "Apple"
    SAMSUNG = "samsung", "Samsung"
    LG = "lg", "LG"
    SONY = "sony", "Sony"
    XIAOMI = "xiaomi", "Xiaomi"
    HUAWEI = "huawei", "Huawei"
    NOKIA = "nokia", "Nokia"
    OPPO = "oppo", "Oppo"
    VIVO = "vivo", "Vivo"
    REALME = "realme", "Realme"
    LC_WAIKIKI = "lc_waikiki", "LC Waikiki"
    ADIDAS = "adidas", "Adidas"


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
    SIZE_43 = "43", "43"
    SIZE_44 = "44", "44"
    SIZE_45 = "45", "45"

    FREE_SIZE = "free", "Free Size"

class ColorChoices(models.TextChoices):
    BLUE = "Blue", "Blue"
    RED = "Red", "Red"
    GREEN = "Green", "Green"
    BLACK = "Black", "Black"
    WHITE = "White", "White"
    YELLOW = "Yellow", "Yellow"
    ORANGE = "Orange", "Orange"
    PURPLE = "Purple", "Purple"
    BROWN = "Brown", "Brown"
    GRAY = "Gray", "Gray"
    PINK = "Pink", "Pink"
    
class ProductCondition(models.TextChoices):
    NEW = "new", "New"
    USED = "used", "Used"
    LIKE_NEW = "like_new", "Like New"
    REFURBISHED = "refurbished", "Refurbished"
    DAMAGED = "damaged", "Damaged"

class Country(models.Model):
    name = models.CharField(max_length=100)
    slug=models.SlugField(unique=True,blank=True)
    icon=models.FileField(upload_to="images/country_icons")
    is_active=models.BooleanField(default=True)
    
    def save(self, *args,**kwargs):
        
        slug=slugify(self.name)
        
        number=1
        
        while Category.objects.filter(slug=slug).exists():
            slug = slugify(self.name)+  f"{number}"
            number+=1
        self.slug=slug
            
        return super().save(self, *args,**kwargs)
    
    def __str__(self):
        return self.name 


class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    image=models.FileField(upload_to='images/category_image')
    description=models.TextField()
    color=models.CharField(max_length=50,choices=ColorChoices.choices, default=ColorChoices.BLACK)
    is_active=models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.name
    
    def save(self, *args,**kwargs):
        
        slug=slugify(self.name)
        
        number=1
        
        while Category.objects.filter(slug=slug).exists():
            slug = slugify(self.name)+  f"{number}"
            number+=1
        self.slug=slug
            
        return super().save(self, *args,**kwargs)
    
    
class ProductCategory(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='product_categories')
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args,**kwargs):
        
        slug=slugify(self.name)
        
        suffix=choices(ascii_letters+digits, k=randint(5,20))
        shuffle(suffix)
        slug+= "".join(suffix)
        
        # number=1
        
        # while ProductCategory.objects.filter(slug=slug).exists():
        #     slug = slugify(self.name)+  f"{number}"
        #     number+=1
        self.slug=slug
            
        # return super().save(*args,**kwargs)




class Product(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    main_image = models.ImageField(upload_to='products/main')
    price = models.BigIntegerField()
    discount = models.PositiveSmallIntegerField(default=0)
    country = models.ForeignKey( Country, on_delete=models.SET_NULL, null=True )
    product_category = models.ForeignKey(  ProductCategory,  on_delete=models.CASCADE,  related_name='products' )
    quantity = models.PositiveIntegerField(default=0)
    review = models.PositiveIntegerField(default=0)
    year = models.SmallIntegerField()
    delivery_time = models.CharField(max_length=50)
    star = models.PositiveSmallIntegerField(default=0)
    company = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    color = models.CharField( max_length=50, choices=ColorChoices.choices, default=ColorChoices.BLACK )
    verified = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)
    condition = models.CharField( max_length=20,choices=[('new', 'New'), ('used', 'Used')] )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    
    def save(self, *args,**kwargs):
        
        slug=slugify(self.name)
        
        number=1
        
        while Category.objects.filter(slug=slug).exists():
            slug = slugify(self.name)+  f"{number}"
            number+=1
        self.slug=slug
            
        return super().save(self, *args,**kwargs)

class ProductImage(models.Model):
    image=models.FileField(upload_to="images/product_images")
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.title} image" 
    
class Service(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    image=models.FileField(upload_to='images/service')
    desc=models.TextField()
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    def save(self, *args,**kwargs):
        
        slug=slugify(self.name)
        
        number=1
        
        while Category.objects.filter(slug=slug).exists():
            slug = slugify(self.name)+  f"{number}"
            number+=1
        self.slug=slug
            
        return super().save(self, *args,**kwargs)

    
    
    
 

    

    
            

            
            
        