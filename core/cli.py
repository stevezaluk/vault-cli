from argparse import ArgumentParser

from vault_lib.core.file import LocalFile
from vault_lib.server.server import VAULTServer, LocalVAULTServer

class CommandLineInterface(ArgumentParser):
    def __init__(self):
        super(CommandLineInterface, self).__init__()

        self._args = None
        self._server = None
    
    def _build_args(self):
        self.add_argument("--direct", action="store_true")
        self.add_argument("--config", action="store")

    def _parse_args(self):
        self._args = self.parse_args()

        if self._args.config:
            pass

        if self._args.direct:
            pass

    def go(self):
        self._build_args()
        self._parse_args()

    def usage(self):
        print("vault-cli : A command line tool to manage VAULT\n")
        print("Basic Operations: ")
        print("\t-h, --help : Print this page")
        print("VAULT Account: ")
        print("\t-l, --login : Login to your VAULT account")
        print("\t-L, --logout : Logout fo your VAULT account")
        print("\t-r, --register : Register someone for a VAULT account")
        print("\t-rv, --revoke USERNAME : Revoke a someones VAULT account")
        print("Content Discovery: ")
        print("\t-i, --info TERM : Get a file by: filename, sha256, insertid, file_id")
        print("\t-s, --search TERM : Search for a file")
        print("\t-I, --index : List all files available for download")
        print("Content Management: ")
        print("\t-a, --archive [term] : Archive a hosted file")
        print("\t-u, --upload SECTION PATH : Upload files")
        print("\t-d, --download TERM : Download files")
        print("\t-U, --update TERM NEW_PATH : Update a path with new files")
        print("\t-m, --metrics [basic/recomendations/user/files/net/all]: View metrics about the content hosted on VAULT")
        print("\n-S, --standards [upload/download] : View uploading standards for your server")
        print("\t-V, --validate PATH : Validate a path/file against current uploading standards")
        print("\t-ss, --sections : View all sections")
        print("\t-sc, --section-create [section_name] : Create a new section")
        print("\t-sr, --section-remove [section_name] : Remove a section")
        print("VPKG Management: ")
        print("\t-v, --vpkg PACKAGE_NAME : Fetch information on a VPKG package")
        print("\t-vad, --vault-auto-download : Run vault-auto-download and update hosted software")
        print("Modifiers: ")
        print("\t--config [.env] : Specify your config file. Default is .env")
        print("\t--direct : Directly connect to resources")
        print("\t--limit [5] : Limit how many results you recieve")
        print("\t--section [section_name] : Search within a section")

