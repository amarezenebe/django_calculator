import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY='v@fx3p8(thfv48qob7int_k4kp+i' \
           'yx^h64pn8j-1iuk88cwue#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=True

ALLOWED_HOSTS=['*']

# coustem user model
AUTH_USER_MODEL='accounts.User'

# Application definition

USER_CAN_ATTEMPT={}
INSTALLED_APPS=[
    "accounts",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

]

MIDDLEWARE=[
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',

]

ROOT_URLCONF='django_calculator.urls'

TEMPLATES=[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION='django_calculator.wsgi.application'

DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS=[
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
# LANGUAGE_CODE = 'en-us'


LANGUAGE_CODE='en-us'

TIME_ZONE='UTC'

USE_I18N=True

USE_L10N=True

USE_TZ=True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL='/static/'

MEDIA_URL='/media/'

LOCAL_STATIC_CDN_PATH=os.path.join(os.path.dirname(BASE_DIR), "static_cdn")
STATIC_ROOT=os.path.join(LOCAL_STATIC_CDN_PATH, 'static')

MEDIA_ROOT=os.path.join(LOCAL_STATIC_CDN_PATH, 'media')

# --------------------------------------------------------------
SIGN_UP_FIELDS=('nick', 'first_name', "last_name")

"""if the user already join the url"""
# LOGIN_REDIRECT_URL='accounts:profile'
LOGIN_URL='accounts:login'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
