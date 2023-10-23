# Setup Dev Environment
1. Create containing folder
2. Set virtual environment `python -m venv <virtual environment name>`
3. Active virtual environment `.\venv\Scripts\activate`
4. Install Django `python -m pip install Django`

# Start Django Project
1. Create Django project `django-admin startproject <project name> .`
2. Run server `python manage.py runserver`
3. Goto http://localhost:8000/

# Setup admin site
1. `python manage.py migrate`
2. `python manage.py createsuperuser`
3. Enter credentials for admin
4. Goto http://localhost:8000/admin/

# Add an app
1. Create app `python manage.py startapp <app name>`
2. Add app to project 
    ```python
    #<project name>/settings.py
    
         INSTALLED_APPS = [
            "<app name>.apps.<app name>Config",
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
        ]
    ```
   
## Create models
1. Build out **\<app name>/models.py**. ie
   ```python
   class Post(models.Model):
       title = models.CharField(max_length=255)
       body = models.TextField()
       created_on = models.DateTimeField(auto_now_add=True)
       last_modified = models.DateTimeField(auto_now=True)
       categories = models.ManyToManyField("Category", related_name="posts")
   
       def __str__(self):
           return self.title
   ```
2. Rename models on admin with (adds an 's' by default)
    ```python
        class Meta:
            verbose_name_plural: "<plural form>"
    ```
3. Define a string return for readability on admin page
    ```python
        def __str__(self):
            return self.<name>
    ```

## Migrate models
1. `python manage.py makemigrations <app name>`
2. `python manage.py migrate <app name>`

## Register models
1. In **\<app name>/admin.py** import the models
2. Define empty admin classes
3. register the models with the admin classes
    ```
    # <app name>/admin.py
    
    from django.contrib import admin
    from <app name>.models import <Model1>, <Model2>, ...
    
    class <Model1>Admin(admin.ModelAdmin):
        pass
    
    class <Model2>Admin(admin.ModelAdmin):
        pass
    
    admin.site.register(<Model1>, <Model1>Admin)
    admin.site.register(<Model2>, <Model2>Admin)
    ```
   
## Generate Data
1. Use the http://localhost:8000/admin/ to generate data

## Build the Views
1. In the **\<app name>/views.py** build out logic for each page ie
    ```python
    # <app name>/views.py
    
    def blog_detail(request, pk):
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        context = {
            "post": post,
            "comments": comments,
        }
    
        return render(request, "blog/detail.html", context)
    ```

## Build the Templates
Each referenced template needs to exist the convention is to place them in
`<app name>/templates/<app name>` to avoid conflicts with similarly named pages

## Include Routes for URLs
1. Create **\<app name>/urls.py**
2. Create a pattern to link an app url route to its correct page. ie
    ```python
    # blog/urls.py
    
    from django.urls import path
    from . import views
    
    urlpatterns = [
        path("", views.blog_index, name="blog_index"),
        path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
        path("category/<category>/", views.blog_category, name="blog_category"),
    ]
    ```
3. Add the app specific urls to the projects urls located in **\<project name>/urls.py**. ie
    ```python
    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path("", include("blog.urls")),
    ]
    ```

## Create forms
1. Create **\<app name>/forms.py**.
2. Create form class. The widget is used to generate the appropriate interface.
   ```python
   from django import forms
   
   class CommentForm(forms.Form):
       author = forms.CharField(
           max_length=60,
           widget=forms.TextInput(
               attrs={"class": "form-control", "placeholder": "Your Name"}
           ),
       )
       body = forms.CharField(
           widget=forms.Textarea(
               attrs={"class": "form-control", "placeholder": "Leave a comment!"}
           )
       )
   ```