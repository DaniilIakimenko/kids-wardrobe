from django.db import models
from django.conf import settings


class Category(models.Model):
    """Категория вещи (Кофты, Штаны и т.д.)"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("URL-слаг", unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Child(models.Model):
    """Профиль ребенка"""
    class Gender(models.TextChoices):
        BOY = 'boy', 'Мальчик'
        GIRL = 'girl', 'Девочка'

    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name="Родитель"
    )
    name = models.CharField("Имя", max_length=100)
    birth_date = models.DateField("Дата рождения")
    gender = models.CharField(
        "Пол",
        max_length=10,
        choices=Gender.choices,
        default=Gender.BOY
    )
    avatar = models.ImageField(
        "Фото",
        upload_to='children_avatars/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Ребенок"
        verbose_name_plural = "Дети"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_gender_display()})"


class ClothingItem(models.Model):
    """Вещь в гардеробе"""
    
    class Season(models.TextChoices):
        WINTER = 'winter', 'Зима'
        SUMMER = 'summer', 'Лето'
        DEMI = 'demi', 'Деми'
        ALL_SEASON = 'all_season', 'Всесезон'

    class Condition(models.TextChoices):
        NEW = 'new', 'Новое'
        EXCELLENT = 'excellent', 'Отличное'
        USED = 'used', 'Б/у'

    class Status(models.TextChoices):
        WEARING = 'wearing', 'Носим'
        SMALL = 'small', 'Мало'
        SELL_GIVE = 'sell_give', 'Продать/Отдать'

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name='clothes',
        verbose_name="Ребенок"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='items',
        verbose_name="Категория"
    )
    name = models.CharField("Название", max_length=200)
    size = models.CharField("Размер (рост)", max_length=10)
    
    season = models.CharField(
        "Сезон",
        max_length=20,
        choices=Season.choices,
        default=Season.DEMI
    )
    condition = models.CharField(
        "Состояние",
        max_length=20,
        choices=Condition.choices,
        default=Condition.NEW
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.WEARING
    )
    
    photo = models.ImageField("Фото", upload_to='clothes_images/')
    notes = models.TextField("Примечания", blank=True, null=True)
    purchase_price = models.DecimalField(
        "Стоимость покупки",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.size} см) - {self.child.name}"