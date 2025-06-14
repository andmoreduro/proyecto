import os

default_title = "<TITLE>"
default_author = "<AUTHOR>"
default_affiliation = "<AFFILIATION>"
default_course = "<COURSE>"
default_instructor = "<INSTRUCTOR>"
default_due_date = "<DUE_DATE>"
default_content = "<CONTENT>"
template_path = os.path.join("templates", "APA")
fonts_name = "fonts"
input_name = "main"
output_name = input_name
fonts_path = os.path.join(fonts_name)
input_path = os.path.join(template_path, f"{input_name}.typ")
output_path = os.path.join(template_path, f"{output_name}.pdf")
typst_process_name = "typst"
typst_process_arguments = ["watch", input_path, output_path, "--font-path", fonts_path]
