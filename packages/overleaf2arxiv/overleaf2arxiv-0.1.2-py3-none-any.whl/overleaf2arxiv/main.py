import argparse
import os
import tempfile

import pyoverleaf

def get_args():
    parser = argparse.ArgumentParser(description="Package an Overleaf project as an arXiv-compatible zip file")
    parser.add_argument("project_id", help="The Overleaf project ID (visible in the URL)")
    parser.add_argument("out_path", help="The path to save the output zip file")
    return parser.parse_args()

def main():
    args = get_args()

    api = pyoverleaf.Api()
    api.login_from_browser()

    out_path = os.path.abspath(args.out_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = os.path.join(temp_dir, "project.zip")
        print("Downloading project...")
        api.download_project(args.project_id, project_path)
        print("Done! Now packaging...")
        cwd = os.getcwd()
        os.chdir(temp_dir)
        try:
            os.system("unzip project.zip")
            os.system("pdflatex main.tex")
            os.system("bibtex main")
            os.system("pdflatex main.tex")
            os.system("pdflatex main.tex")
            os.system(f"zip -r {out_path} . -x project.zip main.log main.out main.blg main.aux main.pdf")
        except Exception as e:
            print(e)
        finally:
            os.chdir(cwd)

if __name__ == "__main__":
    main()
