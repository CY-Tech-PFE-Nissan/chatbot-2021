from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="chatbotapi",
    version="0.0",
    description="Chatbot API for MyNissan app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "django",
        "django-heroku",
        "nltk",
        "gunicorn",
        "whitenoise",
        "dj-database-url",
        "psycopg2",
        "numpy",
        "pandas",
        "torch",
        "torchvision",
        "transformers",
        "fontawesome-free",
        "Pillow",
        "opencv-python",
        "scipy",
        "SpeechRecognition",
        "gTTS",
    ],
    packages=find_packages(),
)
