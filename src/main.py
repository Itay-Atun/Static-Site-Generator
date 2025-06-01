import os, shutil, sys
from markdown_blocks import *


def copy_static_to_public(to_dir, from_dir):

    if os.path.exists(to_dir) and len(os.listdir(to_dir)) > 0:
        print(f"{to_dir} => Exists and full:\n{os.listdir(to_dir)}\nRemoving file...")
        shutil.rmtree(to_dir)
    try:
        os.mkdir(to_dir)
    except FileExistsError:
        print(f"Directory {to_dir} existing, skipping creation...")

    static_files = os.listdir(from_dir)
    count = 1
    for static_file in static_files:
        print(f"{count} => {from_dir}/{static_file} | Is file? = {os.path.isfile(f'{from_dir}/{static_file}')}")
        if not os.path.isfile(f"{from_dir}/{static_file}"):
            try:
                os.mkdir(f"{to_dir}/{static_file}")
                copy_static_to_public(f"{to_dir}/{static_file}", f"{from_dir}/{static_file}")
            except FileExistsError:
                raise FileExistsError(f"{to_dir}/{static_file} exists")
                print(f"{to_dir}/{static_file} exists")
        else:
            shutil.copy(f"{from_dir}/{static_file}", to_dir)
            print(f"Copying {static_file} to {to_dir}")
        count += 1

def generate_page(from_path, template_path, dest_path, base_url):
    print(f"\nGenerating page from {from_path} to {dest_path} using {template_path}")
    
    markdown_text_file = open(from_path, "r")
    markdown_text = markdown_text_file.read()
    markdown_text_file.close()

    title = extract_title(markdown_text)

    html_template_file = open(template_path, "r")
    template_html = html_template_file.read()
    html_template_file.close()

    html_node_str = markdown_to_html_node(markdown_text).to_html()
    index_html = template_html.replace("{{ Title }}", title).replace("{{ Content }}", html_node_str)
    print(index_html.replace('href="', f'href="{base_url}').replace('src="', f'src="{base_url}').replace("/Static-Site-Generator/index.css", "/index.css"))


    try:
        index_html_file = open(dest_path, "x")
    except FileExistsError:
        raise FileExistsError("File already exists... Continuing")

    try:    
        with open(dest_path, "w") as index_html_file:
            index_html_file.write(index_html)
            index_html_file.close()
        return "File Creating sucessfully..."
    except Exception as error:
        raise Exception("Something went wrong... error")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_url):
    content_dir_files = os.listdir(dir_path_content)

    count = 1
    for content_file in content_dir_files:
        if not os.path.isfile(f"{dir_path_content}/{content_file}") and not os.path.exists(f"{dest_dir_path}/{content_file}"):
            os.mkdir(f"{dest_dir_path}/{content_file}")

        print(f"{count} => {dir_path_content}/{content_file} | Is file? = {os.path.isfile(f'{dir_path_content}/index.html')}")
        if os.path.isfile(f"{dir_path_content}/{content_file}"):
            generate_page(f"{dir_path_content}/{content_file}", template_path, f"{dest_dir_path}/index.html", base_url)
        else:
            generate_pages_recursive(f"{dir_path_content}/{content_file}", template_path, f"{dest_dir_path}/{content_file}", base_url)

        count += 1


def main():
    args = sys.argv
    if len(sys.argv) <= 1:
        BASE_URL = "/"
    else:
        BASE_URL = args[1]
    

    copy_static_to_public("/Users/itayat/Learning/BootDev/Static-Site-Generator/docs", "/Users/itayat/Learning/BootDev/Static-Site-Generator/src/static")

    

    print("\n================ Generating Pages =================\n ")
    generate_pages_recursive("/Users/itayat/Learning/BootDev/Static-Site-Generator/content",
                            "/Users/itayat/Learning/BootDev/Static-Site-Generator/src/template.html",
                            "/Users/itayat/Learning/BootDev/Static-Site-Generator/docs", BASE_URL)


    
if __name__ == "__main__":
    main()