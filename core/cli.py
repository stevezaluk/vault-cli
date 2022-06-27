from core.config import Config
from argparse import ArgumentParser

from vault_lib.core.colors import print_error
from vault_lib.core.file import MediaFile, PlexFile
from vault_lib.errors import VAULTFileNotFound
from vault_lib.media_types.game import GameFile

class CommandLineInterface(ArgumentParser):
    def __init__(self):
        super(CommandLineInterface, self).__init__()

        self._args = None

        self._config = Config()
        self._server = self._config.get_connection()
    
    def _build_args(self):
        self.add_argument("-i", "--info", action="store")

        self.add_argument("--config", action="store")
        self.add_argument("--limit", action="store")
        self.add_argument("--direct", action="store_true")
        self.add_argument("-s", "--section", action="store")

    def _parse_args(self):
        self._args = self.parse_args()

        if self._args.config:
            self._config = Config(self._args.config)

        if self._args.direct:
            self._config.get_connection(direct=True)

        if self._args.section:
            section = self._args.section
        else:
            section = None

        if self._args.limit:
            limit = int(self._args.limit)
        else:
            limit = 20

        if self._args.info:
            try:
                file = self._server.get_file(self._args.info, section)
            except VAULTFileNotFound:
                print_error("Failed to find file: ", self._args.info, fatal=True)
            
            print("==> General Info")
            print("File Name: ", file.file_name)
            print("Size: ", file.file_size)
            print("Type: ", file.file_type)
            print("SHA-256: ", file.file_sha)

            print("\n==> Upload Info")
            print("Section: ", file.file_section)
            print("Status: ", file.file_status)
            print("Uploaded By: ", file.uploaded_by)
            print("Uploaded Date: ", file.uploaded_date)
            print("Creation Date: ", file.creation_date)

            if isinstance(file, MediaFile):
                print("==> Media Info")
                print("Resoloution:  ", file.resolution)
                print("Duration: ", file.duration)
                print("Video Codec: ", file.video_codec)
                print("Audio Codec: ", file.audio_codec)
                print("Languages: ", file.languages)

            if isinstance(file, PlexFile):
                print("==> Plex Info")
                print("Title: ", file.title)
                print("Description: ", file.description)
                print("Content Rating: ", file.content_rating)
                print("User Rating: ", file.user_rating)

            if isinstance(file, GameFile):
                print("==> Game Info")
                print("Console: ", file.console)
                print("Region: ", file.region)
                print("Rev: ", file.revelation)

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
        print("\t-S, --search TERM : Search for a file")
        print("\t-I, --index : List all files available for download")
        print("Content Management: ")
        print("\t-a, --archive [term] : Archive a hosted file")
        print("\t-u, --upload SECTION PATH : Upload files")
        print("\t-d, --download TERM : Download files")
        print("\t-U, --update TERM NEW_PATH : Update a path with new files")
        print("\t-m, --metrics [basic/recomendations/user/files/net/all]: View metrics about the content hosted on VAULT")
        # print("\n-S, --standards [upload/download] : View uploading standards for your server")
        print("\t-V, --validate PATH : Validate a path/file against current uploading standards")
        print("\t-s, --section [section_name] : Search within a section")
        print("\t-ss, --sections : View all sections")
        print("VPKG Management: ")
        print("\t-v, --vpkg PACKAGE_NAME : Fetch information on a VPKG package")
        print("\t-vad, --vault-auto-download : Run vault-auto-download and update hosted software")
        print("Modifiers: ")
        print("\t--config [.env] : Specify your config file. Default is .env")
        print("\t--direct : Directly connect to resources")
        print("\t--limit [5] : Limit how many results you recieve")

