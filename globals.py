import os

default_title = "Título"
default_author = "Andrés Felipe Moreno Durango"
default_affiliation = "Universidad Manuela Beltrán"
default_course = "Proyecto de Investigación"
default_instructor = "Hector Miguel Vargas García"
template_path = os.path.join("templates", "APA")
input_name = "main"
output_name = input_name
input_path = os.path.join(template_path, f"{input_name}.typ")
output_path = os.path.join(template_path, f"{output_name}.pdf")
