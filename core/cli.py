from core.config import Config
from argparse import ArgumentParser

from vault_lib.core.colors import print_error
from vault_lib.core.file import MediaFile, PlexFile

from vault_lib.errors import VAULTFileNotFound, VAULTInternalServerError

from vault_lib.media_types.game import GameFile
from vault_lib.media_types.book import Book
from vault_lib.media_types.tv_show import TVShow

class CommandLineInterface(ArgumentParser):
    def __init__(self):
        super(CommandLineInterface, self).__init__()

        self._args = None

        self._config = Config()
        self._server = self._config.get_connection()

    def usage(self):
        print("vault-cli : A command line tool to manage VAULT\n")
        print("Basic Operations: ")
        print("\t-h, --help : Print this page")
        print("Account: ")
        print("\t-l, --login : Login to your VAULT account")
        print("\t-L, --logout : Logout fo your VAULT account")
        print("\t-r, --register : Register someone for a VAULT account")
        print("\t-rv, --revoke USERNAME : Revoke a someones VAULT account")
        print("Discovery: ")
        print("\t-i, --info TERM : Get a file by: filename, sha256, ObjectId, file_id")
        print("\t-S, --search TERM : Search for a file")
        print("\t-I, --index : List all files available for download")
        print("Management: ")
        print("\t-a, --archive TERM : Archive a hosted file")
        print("\t-u, --upload SECTION_NAME PATH : Upload files")
        print("\t-d, --download TERM : Download files")
        print("\t-U, --update TERM NEW_PATH : Update a path with new files")
        print("\t-m, --metrics [basic/recomendations/user/files/net/all]: View metrics about the content hosted on VAULT")
        # print("\n-S, --standards [upload/download] : View uploading standards for your server")
        print("\t-V, --validate PATH : Validate a path/file against current uploading standards")
        print("\t-s, --section SECTION_NAME : Search within a section")
        print("\t-ss, --sections : View all sections")
        print("VPKG Management: ")
        print("\t-v, --vpkg PACKAGE_NAME : Fetch information on a VPKG package")
        print("\t-vad, --vault-auto-download : Run vault-auto-download and update hosted software")
        print("Modifiers: ")
        print("\t--limit [5] : Limit how many results you recieve")
        print("\t--key [key] : Only return the value of a specific key in a document")
        print("\t--no-plex : Skip plex calls i.e. dont include plex data with http responses")
        print("\t--config [.env] : Specify your config file. Default is .env")
        print("\t--direct : Directly connect to resources")
        print("\t--no-upload : Do everything on an upload except upload the file")
    
    def _build_args(self):
        self.add_argument("-i", "--info", action="store")
        self.add_argument("-I", "--index", action="store_true")
        self.add_argument("-ss", "--sections", action="store_true")
        self.add_argument("-S", "--search", action="store")

        self.add_argument("--config", action="store")
        self.add_argument("--limit", action="store", type=int, default=5)
        self.add_argument("--key", action="store", type=str)
        self.add_argument("--no-plex", action="store_true")
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

        if self._args.sections:
            sections = self._server.get_sections(self._args.limit)
            for section in sections:
                print("==> Section")
                print("Name: ", section.section_name)
                print("Path: ", section.section_path)
                print("Type: ", section.section_type)
                print("Total File: ", section.total_files)
                print("Total Downloads: ", section.total_downloads)
                print("Total Uploads: ", section.total_uploads)
                print("Total Archives: ", section.total_archives)
                print("\n")

        # {"file_name":"AVENGERS.mkv", "file_size":10000, "file_type":"Media File", "file_sha":"aaaaaaaaaaaaaa", "file_section":"movies", "file_status":"working", "uploaded_by":"vault", "uploaded_date":"March 5, 2020 01:56:00 PM", "creation_date":"March 5, 2020 01:56:00 PM", "media_info":{"resolution":"1920x1080", "duration":"1h 0m 0s", "video_codec":"HEVC", "video_codec_lib": "x265", "audio_codec":"AAC", "languages":"en"}}

        if self._args.index:
            index = self._server.index(self._args.section, self._args.limit)
            print("==> Index")
            for result in index:
                print("{n} ({s})".format(n=result.file_name, s=result.file_sha))

        if self._args.search:
            search = self._server.search(self._args.search, self._args.section, self._args.limit)
            print("==> Search: ", self._args.search)
            for result in search:
                print("{n} ({s})".format(n=result.file_name, s=result.file_sha))

        if self._args.info:
            try:
                file = self._server.get_file(self._args.info, section)
            except VAULTFileNotFound:
                print_error("Failed to find file: ", self._args.info, fatal=True)
            
            print("==> General Info")
            print("File Name: ", file.file_name)
            # print("Remote Path: ", file.full_path)
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
                print("\n==> Media Info")
                print("Resoloution:  ", file.resolution)
                print("Duration: ", file.duration)
                print("Video Codec: ", file.video_codec)
                print("Audio Codec: ", file.audio_codec)
                print("Languages: ", file.languages)

                if isinstance(file, PlexFile):
                    print("\n==> Plex Info")
                    print("Title: ", file.title)
                    print("Plex Section: ", file.plex_section)
                    print("Description: ", file.description)
                    print("\nPlex Type: ", file.type)
                    print("Content Rating: ", file.content_rating)
                    print("User Rating: ", file.user_rating)
                    print("Added on Plex: ", file.added_at)
                    print("Updated on Plex: ", file.updated_at)
                    print("View Count: ", file.view_count)

            if isinstance(file, GameFile): # build support in generate_object
                print("\n==> Game Info")
                print("Console: ", file.console)
                print("Region: ", file.region)
                print("Rev: ", file.rev)
            
            if isinstance(file, Book):
                print("\n==> Book Info")
                print("Title: ", file.book_title)
                print("Author: ", file.book_author)
                print("Format: ", file.book_format)
                print("Page Count: ", file.page_count)

            if isinstance(file, TVShow):
                print("\n==> TV Info")
                print("Real Season Count: ", file.season_count)
                print("Real Episode Count: ", file.episode_count)
                print("Average Duration (per episode): ", file.average_duration)
    
    def go(self):
        self._build_args()
        self._parse_args()