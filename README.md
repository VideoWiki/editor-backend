Clone the project.
Install the python of version 3.8 .
Install the visual code or pycharm or any python IDE.
Open the project in visual code studio or any IDE.
Install all required packages , run the command in the terminal , pip install -r requirements.txt
Install the system requirements.
# image magic problem
#Check for the ImageMagick policy file. ImageMagick does not have the proper permission set:
#/etc/ImageMagick-6/policy.xml
#comment out (or remove the line that reads)
#<policy domain="path" rights="none" pattern="@*" />
#
#<!-- <policy domain="path" rights="none" pattern="@*" /> -->

sudo apt-get update
sudo apt install imagemagick
sudo apt-get install ffmpeg
sudo apt-get install python-numpy libicu-dev
python3 -m spacy download en_core_web_sm #spacy should be installed first pip3 install spacy
pip3 install asgiref==3.1.2
sudo add-apt-repository ppa:libreoffice/ppa
sudo apt update
sudo apt install libreoffice

# folder required for video editor trim
# media/editor/trim
All the required packages will be installed . After the successful installation , run the command in the terminal , python manage.py makemigrations. 
After completing the makemigrations, run the command in the terminal , python manage.py migrate
After completing the migrate, run the command in the terminal , python manage.py runserver.
The project will running in the localhost.